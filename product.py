from category import Category
from connect import Database
from data import Data
from store import Store


class Product:
    """
    managing products
    """

    def __init__(self,
                 id,
                 brands,
                 name,
                 image,
                 url,
                 description,
                 nutriscore,
                 stores,
                 categories):
        self.id = id
        self.brands = brands
        self.name = name
        self.image = image
        self.url = url
        self.description = description
        self.nutriscore = nutriscore
        self.stores = stores
        self.categories = categories

    @staticmethod
    def importing():
        """
        used for products importing on database
        """
        categories = Database().load('categories')
        for category in categories:
            products = Data(category[3] + '.json').load()
            for product in products:
                if 'stores' in product.keys() \
                        and 'nutriscore_grade' in product.keys() \
                        and 'ingredients_text_fr' in product.keys() \
                        and 'image_url' in product.keys():
                    Product(None,
                            product['brands'],
                            product['product_name'],
                            product['image_url'],
                            product['url'],
                            product['ingredients_text_fr'],
                            product['nutriscore_grade'],
                            product['stores_tags'],
                            product['categories_tags']).save()

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
    def get(product_id):
        """
        get product from a product id
        """
        cur = Database.createCursor()
        cur.execute("""
        SELECT *
        FROM products
        WHERE id = %s """, (product_id,))
        product = cur.fetchone()
        products = Product(product[0],
                           product[6],
                           product[1],
                           product[2],
                           product[3],
                           product[5],
                           product[4],
                           None,
                           None)
        return products

    @staticmethod
    def listing(products):
        """
        display bulleted list of products
        """
        for product in products:
            print('{} - {} - {}'.format(product['id'],
                                        product['product'].brands,
                                        product['product'].name))

    @staticmethod
    def load(category):
        """
        load products from a specific categories
        """
        products_with_id = list()
        i = 1
        cur = Database.createCursor()
        cur.execute("""SELECT product_id
                        FROM categories_products
                        WHERE category_id = %s""", (category,))
        product_id = cur.fetchall()
        for id in product_id:
            products = dict()
            products['id'] = i
            products['product'] = Product.get(id[0])
            i += 1
            products_with_id.append(products)
        return products_with_id

    def display(self):
        """
        displaying product
        """
        return ('**********************\n'
                'id : {}\n'
                'Marque : {}\n'
                'Nom: {}\n'
                'Image: {}\n'
                'Url: {}\n'
                'Description: {}\n'
                'Nutriscore: {}\n'
                'Magasins: {}\n'
                'Catégories: {}\n'
                '**********************'.format(self.id,
                                                self.brands,
                                                self.name,
                                                self.image,
                                                self.url,
                                                self.description,
                                                self.nutriscore,
                                                Store.load_from_id(
                                                    self.id),
                                                Category.load_from_id(
                                                    self.id)))
