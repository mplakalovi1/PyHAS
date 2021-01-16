import requests
import logging
logging.basicConfig(filename='pyHAS.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class Http:

    def __init__(self, url: str, timeout: float):
        logging.info("Request sent (request url: '{}')".format(url))  # date & time of sending request (in local time)
        self.__response = requests.get(url, timeout=timeout)  # response object
        logging.info("Response received.")  # date & time of response (in local time)

    @property
    def size(self):  # response size in bytes
        return self.__response.headers['Content-Length']

    @property
    def response_time(self):  # response time in seconds
        return self.__response.elapsed.total_seconds()

    @property
    def users_bandwidth(self):  # user's bandwidth [bps]
        return float(self.size) * 8 / float(self.response_time)

    @property
    def content(self):  # content of the response, in unicode
        return self.__response.text

    @property
    def successful(self):  # check if response code is 200 (check if response is successful)
        return self.__response.status_code == 200

    def raise_for_status(self):
        self.__response.raise_for_status()
