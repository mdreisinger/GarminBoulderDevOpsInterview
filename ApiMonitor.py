import requests

class ApiMonitor:
    def __init__(self, url):
        self.url = url

    def get(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            return False
        json = response.json()
        try:
            status = json['status']
        except KeyError:
            return False
        if status != "OK":
            return False