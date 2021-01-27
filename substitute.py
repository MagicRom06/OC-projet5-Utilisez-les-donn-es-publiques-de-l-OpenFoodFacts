from category import Category
from connect import Database
from product import Product


class Substitute:
    """
    class used to manage substitute
    """

    def __init__(self,
                 product_id,
                 brands,
                 name,
                 image,
                 url,
                 description,
                 nutriscore):
        self.product_id = product_id
        self.brands = brands
        self.name = name
        self.image = image
        self.url = url
        self.description = description
        self.nutriscore = nutriscore

    @staticmethod
    def find(user_product):
        """
        used for finding substitute from selected product
        """
        user_product.categories = Category.load_from_id(user_product.id)
        i = 1
        substitute = list()
        cur = Database.createCursor()
        cur.execute("""
        SELECT product_id
        FROM categories_products
        INNER JOIN categories
            ON categories_products.category_id = categories.id
        INNER JOIN products
            ON categories_products.product_id = products.id
        WHERE categories.name = %s
            AND products.nutriscore = 'a' limit 5""",
                    (user_product.categories[0], ))
        for elt in cur.fetchall():
            substituts_with_id = dict()
            substituts_with_id['id'] = i
            substituts_with_id['product'] = Product.get(elt[0])
            substitute.append(substituts_with_id)
            i += 1
        return substitute

    @staticmethod
    def listing(products):
        """
        display bulleted list of substitutes
        """
        for product in products:
            print('Substitut {} -\n{}'.format(product['id'],
                                              product['product'].display()))

    def save(self):
        """
        insert substitute in db
        """
        cur = Database.createCursor()
        sql = """
        INSERT INTO substitutes (
        product_id,
        brands,
        name,
        image,
        url,
        description,
        nutriscore)
        VALUES (%s, %s, %s, %s, %s, %s, %s) """
        val = (self.product_id,
               self.brands,
               self.name,
               self.image,
               self.url,
               self.description,
               self.nutriscore)
        cur.execute(sql, val)
        Database.databaseConnection.commit()

    @staticmethod
    def load():
        """
        load all entries of subsitutes table
        """
        return Database.load('substitutes')
