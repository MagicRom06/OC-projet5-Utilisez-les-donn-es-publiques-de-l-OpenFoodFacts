from category import Category
from connect import Database


class Substitute:
    """
    class used to manage substitute
    """
    def __init__(self, user_product):
        self.product = user_product
        self.categories = Category.load_from_id(self.product.id)

    def find(self):
        """
        used for finding substitute from selected product
        """
        substitute = list()
        cur = Database.createCursor()
        for category in self.categories:
            cur.execute("""
            SELECT product_id
            FROM categories_products
            INNER JOIN categories
                ON categories_products.category_id = categories.id
            INNER JOIN products
                ON categories_products.product_id = products.id
            WHERE categories.name = %s
                AND products.nutriscore = 'a' """, (category, ))
            substitute.append(cur.fetchall())
        print(substitute)
