""" Python SDK for JupiterOne GraphQL API """
# pylint: disable=W0212,no-name-in-module
# see https://github.com/PyCQA/pylint/issues/409

import json
from warnings import warn
from typing import Dict, List

import re
import requests
from requests.adapters import HTTPAdapter, Retry
from retrying import retry

from jupiterone.errors import (
    JupiterOneClientError,
    JupiterOneApiRetryError,
    JupiterOneApiError,
)

from jupiterone.constants import (
    J1QL_SKIP_COUNT,
    J1QL_LIMIT_COUNT,
    QUERY_V1,
    CREATE_ENTITY,
    DELETE_ENTITY,
    UPDATE_ENTITY,
    CREATE_RELATIONSHIP,
    DELETE_RELATIONSHIP,
    CURSOR_QUERY_V1,
)


def retry_on_429(exc):
    """Used to trigger retry on rate limit"""
    return isinstance(exc, JupiterOneApiRetryError)


class JupiterOneClient:
    """Python client class for the JupiterOne GraphQL API"""

    # pylint: disable=too-many-instance-attributes

    DEFAULT_URL = "https://graphql.us.jupiterone.io"

    RETRY_OPTS = {
        "wait_exponential_multiplier": 1000,
        "wait_exponential_max": 10000,
        "stop_max_delay": 300000,
        "retry_on_exception": retry_on_429,
    }

    def __init__(self, account: str = None, token: str = None, url: str = DEFAULT_URL):
        self.account = account
        self.token = token
        self.url = url
        self.query_endpoint = self.url
        self.rules_endpoint = self.url + "/rules/graphql"
        self.headers = {
            "Authorization": "Bearer {}".format(self.token),
            "JupiterOne-Account": self.account,
        }

    @property
    def account(self):
        """Your JupiterOne account ID"""
        return self._account

    @account.setter
    def account(self, value: str):
        """Your JupiterOne account ID"""
        if not value:
            raise JupiterOneClientError("account is required")
        self._account = value

    @property
    def token(self):
        """Your JupiterOne access token"""
        return self._token

    @token.setter
    def token(self, value: str):
        """Your JupiterOne access token"""
        if not value:
            raise JupiterOneClientError("token is required")
        self._token = value

    # pylint: disable=R1710
    @retry(**RETRY_OPTS)
    def _execute_query(self, query: str, variables: Dict = None) -> Dict:
        """Executes query against graphql endpoint"""

        data = {"query": query}
        if variables:
            data.update(variables=variables)

        # Always ask for variableResultSize
        data.update(flags={"variableResultSize": True})

        # initiate requests session and implement retry logic of 5 request retries with 1 second between
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        response = s.post(
            self.query_endpoint, headers=self.headers, json=data, timeout=60
        )

        # It is still unclear if all responses will have a status
        # code of 200 or if 429 will eventually be used to
        # indicate rate limits being hit.  J1 devs are aware.
        if response.status_code == 200:
            if response._content:
                content = json.loads(response._content)
                if "errors" in content:
                    errors = content["errors"]
                    if len(errors) == 1:
                        if "429" in errors[0]["message"]:
                            raise JupiterOneApiRetryError(
                                "JupiterOne API rate limit exceeded"
                            )
                    raise JupiterOneApiError(content.get("errors"))
                return response.json()

        elif response.status_code == 401:
            raise JupiterOneApiError(
                "401: Unauthorized. Please supply a valid account id and API token."
            )

        elif response.status_code in [429, 503]:
            print(response.status_code)
            print(response.content)
            raise JupiterOneApiRetryError("JupiterOne API rate limit exceeded.")

        elif response.status_code in [504]:
            raise JupiterOneApiRetryError("Gateway Timeout.")

        elif response.status_code in [500]:
            raise JupiterOneApiError("JupiterOne API internal server error.")

        else:
            content = response._content
            if isinstance(content, (bytes, bytearray)):
                content = content.decode("utf-8")
            if "application/json" in response.headers.get("Content-Type", "text/plain"):
                data = json.loads(content)
                content = data.get("error", data.get("errors", content))
            raise JupiterOneApiError("{}:{}".format(response.status_code, content))

    def _cursor_query(
        self, query: str, cursor: str = None, include_deleted: bool = False
    ) -> Dict:
        """Performs a V1 graph query using cursor pagination
        args:
            query (str): Query text
            cursor (str): A pagination cursor for the initial query
            include_deleted (bool): Include recently deleted entities in query/search
        """

        # If the query itself includes a LIMIT then we must parse that and check if we've reached
        # or exceeded the required number of results.
        limit_match = re.search(r"(?i)LIMIT\s+(?P<inline_limit>\d+)", query)

        if limit_match:
            result_limit = int(limit_match.group("inline_limit"))
        else:
            result_limit = False

        results: List = []
        while True:
            variables = {"query": query, "includeDeleted": include_deleted}

            if cursor is not None:
                variables["cursor"] = cursor

            response = self._execute_query(query=CURSOR_QUERY_V1, variables=variables)
            data = response["data"]["queryV1"]["data"]

            # This means it's a "TREE" query and we have everything
            if "vertices" in data and "edges" in data:
                return data

            results.extend(data)

            if result_limit and len(results) >= result_limit:
                # We can stop paginating if we've collected enough results based on the requested limit
                break
            elif (
                "cursor" in response["data"]["queryV1"]
                and response["data"]["queryV1"]["cursor"] is not None
            ):
                # We got a cursor and haven't collected enough results
                cursor = response["data"]["queryV1"]["cursor"]
            else:
                # No cursor returned so we're done
                break

        # If we detected an inline LIMIT make sure we only return that many results
        if result_limit:
            return {"data": results[:result_limit]}

        # Return everything
        return {"data": results}

    def _limit_and_skip_query(
        self,
        query: str,
        skip: int = J1QL_SKIP_COUNT,
        limit: int = J1QL_LIMIT_COUNT,
        include_deleted: bool = False,
    ) -> Dict:
        results: List = []
        page: int = 0

        while True:
            variables = {
                "query": f"{query} SKIP {page * skip} LIMIT {limit}",
                "includeDeleted": include_deleted,
            }
            response = self._execute_query(query=QUERY_V1, variables=variables)

            data = response["data"]["queryV1"]["data"]

            # If tree query then no pagination
            if "vertices" in data and "edges" in data:
                return data

            if len(data) < J1QL_SKIP_COUNT:
                results.extend(data)
                break

            results.extend(data)
            page += 1

        return {"data": results}

    def query_v1(self, query: str, **kwargs) -> Dict:
        """Performs a V1 graph query
        args:
            query (str): Query text
            skip (int):  Skip entity count
            limit (int): Limit entity count
            cursor (str): A pagination cursor for the initial query
            include_deleted (bool): Include recently deleted entities in query/search
        """
        uses_limit_and_skip: bool = "skip" in kwargs.keys() or "limit" in kwargs.keys()
        skip: int = kwargs.pop("skip", J1QL_SKIP_COUNT)
        limit: int = kwargs.pop("limit", J1QL_LIMIT_COUNT)
        include_deleted: bool = kwargs.pop("include_deleted", False)
        cursor: str = kwargs.pop("cursor", None)

        if uses_limit_and_skip:
            warn(
                "limit and skip pagination is no longer a recommended method for pagination. "
                "To read more about using cursors checkout the JupiterOne documentation: "
                "https://docs.jupiterone.io/features/admin/parameters#query-parameterlist",
                DeprecationWarning,
                stacklevel=2,
            )
            return self._limit_and_skip_query(
                query=query, skip=skip, limit=limit, include_deleted=include_deleted
            )
        else:
            return self._cursor_query(
                query=query, cursor=cursor, include_deleted=include_deleted
            )

    def create_entity(self, **kwargs) -> Dict:
        """Creates an entity in graph.  It will also update an existing entity.

        args:
            entity_key (str): Unique key for the entity
            entity_type (str): Value for _type of entity
            entity_class (str): Value for _class of entity
            timestamp (int): Specify createdOn timestamp
            properties (dict): Dictionary of key/value entity properties
        """
        variables = {
            "entityKey": kwargs.pop("entity_key"),
            "entityType": kwargs.pop("entity_type"),
            "entityClass": kwargs.pop("entity_class"),
        }

        timestamp: int = kwargs.pop("timestamp", None)
        properties: Dict = kwargs.pop("properties", None)

        if timestamp:
            variables.update(timestamp=timestamp)
        if properties:
            variables.update(properties=properties)

        response = self._execute_query(query=CREATE_ENTITY, variables=variables)
        return response["data"]["createEntity"]

    def delete_entity(self, entity_id: str = None) -> Dict:
        """Deletes an entity from the graph.  Note this is a hard delete.

        args:
            entity_id (str): Entity ID for entity to delete
        """
        variables = {"entityId": entity_id}
        response = self._execute_query(DELETE_ENTITY, variables=variables)
        return response["data"]["deleteEntity"]

    def update_entity(self, entity_id: str = None, properties: Dict = None) -> Dict:
        """
        Update an existing entity.

        args:
            entity_id (str): The _id of the entity to update
            properties (dict): Dictionary of key/value entity properties
        """
        variables = {"entityId": entity_id, "properties": properties}
        response = self._execute_query(UPDATE_ENTITY, variables=variables)
        return response["data"]["updateEntity"]

    def create_relationship(self, **kwargs) -> Dict:
        """
        Create a relationship (edge) between two entities (vertices).

        args:
            relationship_key (str): Unique key for the relationship
            relationship_type (str): Value for _type of relationship
            relationship_class (str): Value for _class of relationship
            from_entity_id (str): Entity ID of the source vertex
            to_entity_id (str): Entity ID of the destination vertex
        """
        variables = {
            "relationshipKey": kwargs.pop("relationship_key"),
            "relationshipType": kwargs.pop("relationship_type"),
            "relationshipClass": kwargs.pop("relationship_class"),
            "fromEntityId": kwargs.pop("from_entity_id"),
            "toEntityId": kwargs.pop("to_entity_id"),
        }

        properties = kwargs.pop("properties", None)
        if properties:
            variables["properties"] = properties

        response = self._execute_query(query=CREATE_RELATIONSHIP, variables=variables)
        return response["data"]["createRelationship"]

    def delete_relationship(self, relationship_id: str = None):
        """Deletes a relationship between two entities.

        args:
            relationship_id (str): The ID of the relationship
        """
        variables = {"relationshipId": relationship_id}

        response = self._execute_query(DELETE_RELATIONSHIP, variables=variables)
        return response["data"]["deleteRelationship"]
