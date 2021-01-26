import json
import ssl
import urllib.request


class Data:
    def __init__(self, url):
        self.url = url

    def load(self):
        """
        method for getting all the data from API
        return list of all api data selected
        """
        scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        url = self.url
        response = urllib.request.urlopen(url, context=scontext)
        data = json.loads(response.read().decode('UTF-8'))
        for key, value in data.items():
            if key == 'tags':
                return value
            elif key == 'products':
                return value

    @staticmethod
    def filter(data):
        """
        filter data to get only the four biggest categories
        return list of filtered categories
        """
        data = [x for x in sorted(data, key=lambda x: x['products'],
                                  reverse=True)][:30]
        return data
