from connect import Database
from data import Data


class Store:
    """
    managing stores
    """
    def __init__(self, name):
        self.name = name

    @staticmethod
    def importing():
        """
        used for stores importing on database ordered by abc
        """
        store_list = list()
        stores = Data('https://fr.openfoodfacts.org/stores.json').load()
        for store in stores:
            store_list.append(store['id'])
        store_list = sorted(store_list)
        for elt in store_list:
            Store(elt).save()

    def save(self):
        """
        Used for inserting stores on database
        """
        cur = Database.createCursor()
        sql = """
        INSERT
        INTO stores (name)
        VALUES (%s) """
        val = (self.name, )
        cur.execute(sql, val)
        Database.databaseConnection.commit()
        print(cur.rowcount, "record inserted.")

    @staticmethod
    def load_from_id(product_id):
        """
        load stores from product id
        """
        cur = Database.createCursor()
        cur.execute("""
        SELECT name
        FROM stores
        INNER JOIN stores_products
            ON stores.id = stores_products.store_id
        WHERE product_id = %s""", (product_id,))
        return [''.join(x) for x in cur.fetchall()]
