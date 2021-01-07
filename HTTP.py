import requests
import time


class Http:
    def __init__(self, url):
        self.response = requests.get(url)

    def getsize(self):  # response size in bytes
        return self.response.headers['Content-Length']

    def getrsptime(self):  # response time in seconds
        return self.response.elapsed.total_seconds()

    def clientbandwidth(self):
        return float(self.getsize())*8/float(self.getrsptime())

    def getcontent(self):  # content of the response, in unicode
        return self.response.text

    def successful(self): #  check if response code is 200 (is response successful)
        return self.response.status_code==200
