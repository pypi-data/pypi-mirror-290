import unittest
from unittest.mock import Mock, patch

from chainalysis.DataSolutions import DataSolutionsClient
from src.chainalysis.util_functions.exceptions import (
    DataSolutionsAPIException,
    InternalServerException,
    UnhandledException,
)

mocked_async_query_id_response = {
    "status": "pending",
    "query_id": "01ef5a51-0e7c-13d6-9383-6412bf7b03cc",
}

mocked_async_query_response_1 = {
    "status": "pending",
    "message": "Query is in a pending state",
}

mocked_async_query_response_2 = {
    "status": "success",
    "results": [{"chain_id": "bip122:000000000019d6689c085ae165831e93"}],
    "stats": {
        "truncated": "false",
        "time": 2317.030191421509,
        "size": 45,
        "total_size": 45,
        "count": 1,
        "starting_row_offset": 0,
        "last_processed_row_offset": 0,
        "total_count": 1,
        "starting_page_index": 0,
        "last_processed_page_index": 0,
        "total_pages": 1,
    },
    "next": "next_url",
}

mocked_async_query_response = {
    "status": "success",
    "results": [{"chain_id": "bip122:000000000019d6689c085ae165831e93"}],
    "stats": {
        "truncated": "false",
        "time": 2317.030191421509,
        "size": 45,
        "total_size": 45,
        "count": 1,
        "starting_row_offset": 0,
        "last_processed_row_offset": 0,
        "total_count": 1,
        "starting_page_index": 0,
        "last_processed_page_index": 0,
        "total_pages": 1,
    },
    "next": "next_url",
}


class AnalyticalTests(unittest.TestCase):
    @patch("api.sql.analytical.issue_request")
    def test_successful_query(self, mocked_issue_request: Mock):
        ds = DataSolutionsClient(
            api_key="",
        )

        first_response = mocked_async_query_id_response
        second_response = mocked_async_query_response_1
        third_response = mocked_async_query_response_2

        mocked_issue_request.side_effect = (
            first_response,
            second_response,
            third_response,
        )

        query_result = ds.sql.analytical("", polling_interval_sec=0)

        self.assertEqual(query_result.query_id, "01ef5a51-0e7c-13d6-9383-6412bf7b03cc")
        self.assertEqual(
            query_result.json(),
            mocked_async_query_response_2["results"],
        )
        self.assertEqual(query_result.stats(), mocked_async_query_response_2["stats"])
        self.assertEqual(query_result.was_successful(), True)
        self.assertEqual(query_result.status_code(), 200)

    @patch("api.sql.analytical.issue_request")
    def test_first_api_exception(self, mocked_issue_request: Mock):
        ds = DataSolutionsClient(
            api_key="",
        )

        mocked_issue_request.side_effect = DataSolutionsAPIException()

        with self.assertRaises(DataSolutionsAPIException):

            ds.sql.analytical("", polling_interval_sec=0)

    @patch("api.sql.analytical.issue_request")
    def test_second_api_exception(self, mocked_issue_request: Mock):
        ds = DataSolutionsClient(
            api_key="",
        )

        mocked_issue_request.side_effect = (
            mocked_async_query_id_response,
            DataSolutionsAPIException(),
        )

        query_result = ds.sql.analytical("", polling_interval_sec=0)

        self.assertEqual(query_result._status, "error")
        self.assertEqual(query_result._status_code, 0)
        self.assertEqual(query_result.was_successful(), False)

        with self.assertRaises(DataSolutionsAPIException):
            query_result.json()

        with self.assertRaises(DataSolutionsAPIException):
            query_result.df()

        with self.assertRaises(DataSolutionsAPIException):
            query_result.stats()

    @patch("api.sql.analytical.issue_request")
    def test_interval_server_exception(self, mocked_issue_request: Mock):
        ds = DataSolutionsClient(
            api_key="",
        )

        mocked_issue_request.side_effect = (
            mocked_async_query_id_response,
            InternalServerException(),
        )

        query_result = ds.sql.analytical("", polling_interval_sec=0)

        self.assertEqual(query_result._status, "error")
        self.assertEqual(query_result._status_code, 500)
        self.assertEqual(query_result.was_successful(), False)

        with self.assertRaises(InternalServerException):
            query_result.json()

        with self.assertRaises(InternalServerException):
            query_result.df()

        with self.assertRaises(InternalServerException):
            query_result.stats()

    @patch("api.sql.analytical.issue_request")
    def test_unhandled_exception(self, mocked_issue_request: Mock):
        ds = DataSolutionsClient(
            api_key="",
        )

        mocked_issue_request.side_effect = (
            mocked_async_query_id_response,
            Exception(),
        )

        query_result = ds.sql.analytical("", polling_interval_sec=0)

        self.assertEqual(query_result._status, "error")
        self.assertEqual(query_result._status_code, 0)
        self.assertEqual(query_result.was_successful(), False)

        with self.assertRaises(UnhandledException):
            query_result.json()

        with self.assertRaises(UnhandledException):
            query_result.df()

        with self.assertRaises(UnhandledException):
            query_result.stats()


if __name__ == "__main__":
    unittest.main()
