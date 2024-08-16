from __future__ import annotations

import requests
from datetime import datetime


class BaseDownloader:
    def __init__(self, base_url=None):
        self.request_counter = 0  # keep track the number of requests considering Bitstamp API limits
        if base_url is not None:
            self.BASE_URL = base_url

    def _get(self, url: str, params: dict | None) -> dict | list | None:
        """
        Perform a GET request to a specified API endpoint
        :param params: params for request
        :return: python dictionary object
        """
        try:
            response = requests.get(url, params=params)
            self.request_counter += 1
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

    def _date_to_timestamp(self, date_string: str) -> int:
        datetime_format = "%Y-%m-%d %H:%M:%S"
        try:

            dt = datetime.strptime(date_string, datetime_format)
            return int(dt.timestamp())
        except ValueError:
            try:
                dt = datetime.strptime(date_string, "%Y-%m-%d")
                return int(dt.timestamp())
            except ValueError as e:
                raise e

    def _reset_request_counter(self) -> None:
        self.request_counter = 0
