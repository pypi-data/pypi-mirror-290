from time import sleep

import pandas as pd

from src.api.constants import ANALYTICAL_ENDPOINTS, BASE_URL
from src.utils.exceptions import raise_exception
from src.utils.requests import send_get_request, send_post_request


class Analytical:
    """
    This class provides methods to execute SQL queries on Data Solutions
    DataBricks tables. It supports fetching results as JSON or a
    pandas DataFrame, and provides query execution statistics.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Analytical class with the provided API key.

        :param api_key: The API key for accessing the analytical service.
        :type api_key: str
        """

        self.api_key = api_key
        self._status_code = 0
        self.error_message = ""
        self.results = {}
        self._stats = {}
        self.json_data = {}
        self.dataframe_data = None
        self.status = ""
        self.next = ""
        self._total_pages = 0

    def __call__(
        self,
        query: str,
        parameters: dict[str] = {},
        polling_interval_sec: int = 5,
    ):
        """
        Execute a SQL query asynchronously using the provided parameters
        and polling interval.

        :param query: The SQL query to be executed.
        :type query: str
        :param parameters: A dictionary of parameters to be used in the query.
        :type parameters: dict[str], optional
        :param polling_interval_sec: The interval in seconds between status checks.
        :type polling_interval_sec: int, optional
        :return: An instance of the Analytical class with query results.
        :rtype: Analytical
        """

        query_execution_url = (
            f"{BASE_URL['base_url']}/{ANALYTICAL_ENDPOINTS['async_query_execution']}"
        )

        body = {
            "sql": query,
            "parameters": parameters,
        }

        response = send_post_request(
            api_key=self.api_key,
            url=query_execution_url,
            body=body,
        )

        if response.status_code != 200:
            raise_exception(response.status_code)

        async_data = response.json()

        if async_data["status"] == "error":
            raise Exception(async_data["message"])

        query_id = async_data["query_id"]

        async_query_status_url = (
            f"{BASE_URL['base_url']}/{ANALYTICAL_ENDPOINTS['async_query_status']}"
        )

        while True:
            response = send_get_request(
                api_key=self.api_key,
                url=async_query_status_url,
                params={"query_id": query_id},
            )
            self._status_code = response.status_code

            if self._status_code != 200:
                raise_exception(self._status_code)

            self.json_data = response.json()
            self._status = self.json_data["status"]

            if self._status == "running" or self._status == "pending":
                sleep(polling_interval_sec)
            if self._status == "error":
                self.error_message = self.json_data["message"]
                self.error_details = self.json_data.get("details")
                return self
            elif self._status == "success":
                self._status = self._status
                self._stats = self.json_data["stats"]
                self.results = self.json_data["results"]
                self.next_url = self.json_data["next"]
                self._total_pages = self._stats["total_pages"]
                return self

    def next_page(self):
        """
        Fetch the next page of DataBricks query results.

        :return: An instance of the Analytical class with the next page of results.
        :rtype: Analytical
        """

        response = send_get_request(
            api_key=self.api_key,
            url=self.next_url,
        )
        self._status_code = response.status_code
        self.json_data = response.json()
        self._status = self.json_data["status"]

        if self._status == "error":
            self.error_message = self.json_data["message"]
            self.error_details = self.json_data.get("details")
            return self
        elif self._status == "success":
            self._status = self._status
            self._stats = self.json_data["stats"]
            self.results = self.json_data["results"]
            self.next_url = self.json_data["next"]
            return self

    def json(self):
        """
        Return results as a JSON.

        :raises Exception: Raises an exception if the query resulted in an error.
        :return: Results of the SQL query as a JSON.
        :rtype: dict
        """

        if self.status != "error":
            return self.results
        else:
            raise Exception(self.error_message)

    def df(self):
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

    def stats(self):
        """
        Get the statistics of the executed query.

        :return: Statistics of the query execution.
        :rtype: dict
        """

        return self._stats

    def status_code(self):
        """
        Get the HTTP status code of the response.

        :return: HTTP status code.
        :rtype: int
        """

        return self._status_code

    def was_successful(self):
        """
        Determine if the query executed successfully.

        :return: True if the query was successful, False otherwise.
        :rtype: bool
        """

        if self.status != "error":
            return True
        return False

    def total_pages(self) -> int:
        """
        Return total number of pages.

        :return: Number of pages.
        :rtype: int
        """

        return self._total_pages
