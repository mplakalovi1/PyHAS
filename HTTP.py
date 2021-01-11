import requests
import logging
logging.basicConfig(filename='pyHAS.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class Http:

    def __init__(self, url, TIMEOUT=5):
        logging.info("Request sent (request url: '{}')".format(url))  # date & time of sending request (in local time)
        self.response = requests.get(url, timeout=TIMEOUT)  # response object
        logging.info("Response received.")  # date & time of response (in local time)

    def getsize(self):  # response size in bytes
        return self.response.headers['Content-Length']

    def getrsptime(self):  # response time in seconds
        return self.response.elapsed.total_seconds()

    def usersbandwidth(self):  # user's bandwidth [bps]
        return float(self.getsize()) * 8 / float(self.getrsptime())

    def getcontent(self):  # content of the response, in unicode
        return self.response.text

    def successful(self):  # check if response code is 200 (check if response is successful)
        return self.response.status_code == 200
