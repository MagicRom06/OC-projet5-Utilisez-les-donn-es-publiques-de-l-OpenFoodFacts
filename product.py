from connect import Database


class Product:
    """
    Used for importing products on database
    """
    def __init__(self,
                 brands,
                 name,
                 image,
                 url,
                 description,
                 nutriscore,
                 stores,
                 categories):
        self.brands = brands
        self.name = name
        self.image = image
        self.url = url
        self.description = description
        self.nutriscore = nutriscore
        self.stores = stores
        self.categories = categories

    def save(self):
        """
        Used for inserting products on database
        """
        db = Database()
        cnx = db.connect()
        cur = cnx.cursor(buffered=True)
        sql = """ INSERT INTO products (
        brand,
        name,
        image,
        url,
        description,
        nutriscore)
        VALUES (%s, %s, %s, %s, %s, %s) """
        val = (self.brands,
               self.name,
               self.image,
               self.url,
               self.description,
               self.nutriscore)
        cur.execute(sql, val)
        last_product_id = cur.lastrowid
        cnx.commit()

        if len(self.stores) > 0 and len(self.categories) > 0:
            for elt in self.stores:
                cur.execute(""" select id from stores
                where name = %s """, (str(elt), ))
                if cur.rowcount:
                    id = cur.fetchone()[0]
                    sql = """ INSERT INTO stores_products
                    (store_id, product_id) VALUES (%s, %s)"""
                    cur.execute(sql, (int(id), int(last_product_id)))
                    cnx.commit()

            for elt in self.categories:
                cur.execute(""" select id from categories
                where url_id = %s """, (str(elt), ))
                if cur.rowcount:
                    id = cur.fetchone()[0]
                    sql = """ INSERT INTO categories_products
                    (category_id, product_id) VALUES (%s, %s) """
                    cur.execute(sql, (int(id), int(last_product_id)))
                    cnx.commit()
