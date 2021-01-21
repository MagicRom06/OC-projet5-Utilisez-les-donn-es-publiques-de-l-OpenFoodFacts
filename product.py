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
        cur = Database.createCursor()
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
        Database.databaseConnection.commit()

        if len(self.stores) > 0 and len(self.categories) > 0:
            for elt in self.stores:
                cur.execute(""" select id from stores
                where name = %s """, (str(elt),))
                if cur.rowcount:
                    id = cur.fetchone()[0]
                    sql = """ INSERT INTO stores_products
                    (store_id, product_id) VALUES (%s, %s)"""
                    cur.execute(sql, (int(id), int(last_product_id)))
                    Database.databaseConnection.commit()

            for elt in self.categories:
                cur.execute(""" select id from categories
                where url_id = %s """, (str(elt),))
                if cur.rowcount:
                    id = cur.fetchone()[0]
                    sql = """ INSERT INTO categories_products
                    (category_id, product_id) VALUES (%s, %s) """
                    cur.execute(sql, (int(id), int(last_product_id)))
                    Database.databaseConnection.commit()

    @staticmethod
    def load(category):
        final_list_product = list()
        i = 1
        cur = Database.createCursor()
        cur.execute("""select product_id from categories_products
                        inner join categories
                         on categories_products.category_id = categories.id
                         where categories.id = %s""", (category,))
        product_id = cur.fetchall()
        for id in product_id:
            product_details = list()
            products_list = list()
            product_with_id = dict()
            cur.execute('select * from products where id = %s', (id[0],))
            product = cur.fetchall()
            cur.execute("""select name from categories
            inner join categories_products
            on categories.id = categories_products.category_id
            where categories_products.product_id = %s""", (id[0],))
            categories = cur.fetchall()
            cur.execute("""select name from stores
            inner join stores_products
            on stores.id = stores_products.store_id
            where stores_products.product_id = %s""", (id[0],))
            stores = cur.fetchall()
            product_details.append(product)
            product_details.append(categories)
            product_details.append(stores)
            products_list.append(product_details)
            for elt in products_list:
                product_with_id['id'] = i
                product_with_id['product'] = elt
                i += 1
            final_list_product.append(product_with_id)
        return final_list_product

    @staticmethod
    def display_list(products):
        for product in products:
            print('{} - {} - {}'.format(product['id'], product['product'][0][0][6], product['product'][0][0][1]))

    def display_one(self):
        print('Marque : {}\n'
              'Nom: {}\n'
              'Image: {}\n'
              'Url: {}\n'
              'Description: {}\n'
              'Nutriscore: {}\n'
              'Magasins: {}\n'
              'Catégories: {}'.format(self.brands,
                                      self.name,
                                      self.image,
                                      self.url,
                                      self.description,
                                      self.nutriscore,
                                      ', '.join(''.join(elt) for elt in self.stores),
                                      ', '.join(''.join(elt) for elt in self.categories)))
