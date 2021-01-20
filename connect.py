from mysql.connector import Error, connect, errorcode


class Database:
    """
    Class used for interacting with the database
    """

    def __init__(self):
        self.config = {
            'user': 'root',
            'password': 'root',
            'host': '127.0.0.1',
            'database': 'openfoodfacts',
            'raise_on_warnings': True
        }

    def connect(self):
        """
        Used for the database connexion
        return cnx or err if an error occured
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
            raise err
        else:
            return cnx

    def load(self, table):
        """
        Used for load table from database
        return all the data from the selected table
        """
        cnx = self.connect()
        cur = cnx.cursor()
        cur.execute(" SELECT * from " + table)
        return cur.fetchall()

    def delete_entries_with_no_fk(self):
        """
        Used for deleting all products row
        with no stores and categories foreign keys
        """
        cnx = self.connect()
        cur = cnx.cursor()
        cur.execute('select product_id from stores_products')
        product_id = cur.fetchall()
        cur.execute('select id from products')
        all_products = cur.fetchall()
        for product in all_products:
            if product not in product_id:
                cur.execute(""" delete from categories_products
                                where product_id = %s""", (product[0],))
                cur.execute("delete from products where id = %s",
                            (product[0],))
                cnx.commit()

