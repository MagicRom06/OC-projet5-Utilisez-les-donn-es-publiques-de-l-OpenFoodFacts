from mysql.connector import Error, connect, errorcode


class Category:
    """
    Class used to get categories data from openfoodfacts data,
    filter it and insert it to mysql database
    """

    def __init__(self, name, count, url, url_id):
        """
        Database information for connexion
        """
        self.name = name
        self.count = count
        self.url = url
        self.url_id = url_id

    def save(self):
        """
        method to insert data into mysql database
        """
        config = {
            'user': 'root',
            'password': 'root',
            'host': '127.0.0.1',
            'database': 'openfoodfacts',
            'raise_on_warnings': True
        }
        try:
            cnx = connect(**config)
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cur = cnx.cursor()
            sql = """ INSERT INTO categories (name, count, url, url_id) VALUES (%s, %s, %s, %s) """
            val = (self.name, self.count, self.url, self.url_id)
            cur.execute(sql, val)
            cnx.commit()
            print(cur.rowcount, "record inserted.")

