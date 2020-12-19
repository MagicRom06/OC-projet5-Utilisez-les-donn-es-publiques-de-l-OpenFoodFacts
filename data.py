import json
import ssl
import urllib.request


class Data:
    def __init__(self, url):
        self.url = url

    def all(self):
        """
        method to get all the data from API
        :return:list
        """
        scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        url = self.url
        response = urllib.request.urlopen(url, context=scontext)
        data = json.loads(response.read().decode('UTF-8'))
        for key, value in data.items():
            if key == 'tags':
                return value

    @staticmethod
    def filter(data):
        """
        filter data to get only the four biggest categories
        :param data:list
        :return:list
        """
        data = [x for x in sorted(data, key=lambda x: x['products'], reverse=True)][:4]
        return data
