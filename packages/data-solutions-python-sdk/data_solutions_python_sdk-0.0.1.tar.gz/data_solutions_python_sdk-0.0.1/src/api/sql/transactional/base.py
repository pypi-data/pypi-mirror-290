import re

import pandas as pd

from src.api.constants import BASE_URL, TRANSACTIONAL_ENDPOINTS
from src.utils.exceptions import raise_exception
from src.utils.requests import send_post_request


class Transactional:
    """
    This class provides methods to handle transactional queries.
    It supports fetching results as JSON or pandas DataFrame,
    and provides query execution statistics.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Transactional object with an API key.

        :param api_key: API key for authenticating requests.
        :type api_key: str
        """
        self.api_key = api_key
        self._status_code = 0
        self.error_message = ""
        self.results = {}
        self._stats = {}
        self.json_data = {}
        self.status = ""
        self.dataframe_data = None

    def __call__(
        self, query: str, parameters: dict[str, str] = {}, options: dict[str, str] = {}
    ):
        """
        Execute a SQL query using the provided parameters and options.

        :param query: SQL query template with placeholders for parameters.
        :type query: str
        :param parameters: Parameters to format the SQL query.
        :type parameters: dict[str, str]
        :param options: Additional options for query execution.
        :type options: dict[str, str]
        :return: Returns self for chaining or method chaining.
        :rtype: Transactional
        """

        query_execution_url = (
            f"{BASE_URL['base_url']}/{TRANSACTIONAL_ENDPOINTS['query_execution']}"
        )

        # Update query with parameters
        parameterized_query = re.sub(
            r"\{\{(\w+)\}\}", lambda m: parameters.get(m.group(1), m.group(0)), query
        )

        body = {
            "sql": parameterized_query,
            "options": options,
        }

        response = send_post_request(
            api_key=self.api_key, url=query_execution_url, body=body
        )
        self._status_code = response.status_code

        if self._status_code != 200:
            raise_exception(self._status_code)

        self.json_data = response.json()
        self.status = self.json_data["status"]

        if self.status == "error":
            self.error_message = self.json_data["message"]
            self.error_details = self.json_data.get("details")
        else:
            self._stats = self.json_data["stats"]
            self.results = self.json_data["results"]

        return self

    def json(self) -> dict:
        """
        Return the JSON data of the results.

        :raises Exception: Raises an exception if the query resulted in an error.
        :return: JSON results of the SQL query.
        :rtype: dict
        """

        if self.status != "error":
            return self.results
        else:
            raise Exception(self.error_message)

    def df(self) -> pd.DataFrame:
        """
        Convert query results into a pandas DataFrame.

        :raises Exception: Raises an exception if the query resulted in an error.
        :return: DataFrame containing the results of the SQL query.
        :rtype: pd.DataFrame
        """
        if self.status != "error":
            if (
                self.dataframe_data
            ):  # Return if data has already been converted to a DataFrame before
                return self.dataframe_data
            self.dataframe_data = pd.DataFrame(self.results)
            return self.dataframe_data
        else:
            raise Exception(self.error_message)

    def stats(self) -> dict:
        """
        Get the statistics of the executed query.

        :return: Statistics of the query execution.
        :rtype: dict
        """
        return self._stats

    def status_code(self) -> int:
        """
        Get the HTTP status code of the response.

        :return: HTTP status code.
        :rtype: int
        """
        return self._status_code

    def was_successful(self) -> bool:
        """
        Determine if the query executed successfully.

        :return: True if the query was successful, False otherwise.
        :rtype: bool
        """
        if self.status != "error":
            return True
        return False
