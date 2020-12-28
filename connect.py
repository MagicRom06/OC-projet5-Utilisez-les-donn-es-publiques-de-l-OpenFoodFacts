from mysql.connector import Error, connect, errorcode


class Database:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': 'root',
            'host': '127.0.0.1',
            'database': 'openfoodfacts',
            'raise_on_warnings': True
        }

    def connect(self):
        try:
            cnx = connect(**self.config)
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            raise err
        else:
            return cnx
