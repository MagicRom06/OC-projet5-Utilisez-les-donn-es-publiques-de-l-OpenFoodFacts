from mysql.connector import Error, connect, errorcode


class Database:
    """
    Class used for interacting with the database
    """
    databaseConnection = None

    @staticmethod
    def connect():
        """
        Used for the database connexion
        return cnx or err if an error occured
        """
        try:
            cnx = connect(user='root',
                          password='root',
                          host='127.0.0.1',
                          database='openfoodfacts',
                          raise_on_warnings=True)
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            raise err
        else:
            Database.databaseConnection = cnx

    @staticmethod
    def disconnect():
        """
        disconnect database
        """
        Database.databaseConnection.close()
        Database.databaseConnection = None

    @staticmethod
    def createCursor():
        """
        create cursor
        """
        return Database.databaseConnection.cursor(buffered=True)

    @staticmethod
    def load(table):
        """
        Used for load table from database
        return all the data from the selected table
        """
        cur = Database.createCursor()
        cur.execute(" SELECT * from " + table)
        entries = cur.fetchall()
        cur.close()
        return entries

    @staticmethod
    def delete_entries_with_no_fk():
        """
        Used for deleting all products row
        with no stores and categories foreign keys
        """
        cur = Database.createCursor()
        cur.execute("""
        SELECT product_id
        FROM stores_products""")
        product_id = cur.fetchall()
        cur.execute("""
        SELECT id
        FROM products""")
        all_products = cur.fetchall()
        for product in all_products:
            if product not in product_id:
                cur.execute("""
                DELETE
                FROM categories_products
                WHERE product_id = %s""", (product[0],))
                cur.execute("""
                DELETE
                FROM products
                WHERE id = %s""", (product[0],))
                Database.databaseConnection.commit()
                cur.close()
        cur.close()

    def is_empty(self):
        """
        check if the table products is empty
        """
        cur = self.createCursor()
        cur.execute(""" SELECT id from products limit 1 """)
        entries = cur.fetchone()
        cur.close()
        if not entries:
            return True
