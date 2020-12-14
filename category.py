import json
import ssl
import urllib.request

from mysql.connector import Error, connect, errorcode


class Category:
    """
    Class used to get categories data from openfoodfacts data,
    filter it and insert it to mysql database
    """
    def __init__(self):
        """
        Database information for connexion
        """
        self.config = {
            'user': 'root',
            'password': 'root',
            'host': '127.0.0.1',
            'database': 'openfoodfacts',
            'raise_on_warnings': True
        }

    def get_all_data(self):
        """
        method to get all the data from API
        :return:list
        """
        scontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        url = 'https://fr.openfoodfacts.org/categories.json'
        response = urllib.request.urlopen(url, context=scontext)
        data = json.loads(response.read().decode('UTF-8'))
        for key, value in data.items():
            if key == 'tags':
                return value

    def filtered_data(self, list):
        """
        filter data to get only the four biggest categories
        :param list:list
        :return:list
        """
        data = [x for x in sorted(list, key=lambda x:x['products'],
                                  reverse=True)][:4]
        return data

    def insert_to_db(self, data):
        """
        method to insert data into mysql database
        :param data:list
        """
        try:
            cnx = connect(**self.config)
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cur = cnx.cursor()
            for line in data:
                sql = """ INSERT INTO categories (name, count, url, url_id)
                      VALUES (%s, %s, %s, %s) """
                val = (line['name'],
                       line['products'],
                       line['url'],
                       line['id'])
                cur.execute(sql, val)
                cnx.commit()
                print(cur.rowcount, "record inserted.")
