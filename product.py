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

    @staticmethod
    def load(category):
        db = Database()
        cnx = db.connect()
        cur = cnx.cursor(buffered=True)
        products = list()
        categories = list()
        cur.execute("""select product_id from categories_products
                        inner join categories
                         on categories_products.category_id = categories.id
                         where categories.id = %s""", (category,))
        product_id = cur.fetchall()
        for id in product_id:
            cur.execute('select * from products where id = %s', (id[0],))
            products.append(cur.fetchall())
        return products

    @staticmethod
    def add_categories(products):
        db = Database()
        cnx = db.connect()
        cur = cnx.cursor(buffered=True)
        for product in products:
            categories_id_list = list()
            categories = list()
            cur.execute("""select category_id from categories_products
            inner join products
            on categories_products.product_id = products.id
            where product_id = %s""", (product[0][0], ))
            category_id = cur.fetchall()
            for id in category_id:
                categories_id_list.append(id[0])
            product.append(categories_id_list)
            for elt in product[1]:
                cur.execute("""select name from categories where id = %s""", (elt, ))
                categories.append(cur.fetchone()[0])
            product.append(categories)
            del(product[1])
        return products

    @staticmethod
    def display(products):
        products_dict = dict()
        i = 1
        for product in products:
            products_dict[i] = product
            i += 1
        for key, value in products_dict.items():
            print('{} - {} - {}'.format(key, value[0][6], value[0][1]))
