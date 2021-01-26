from connect import Database
from data import Data


class Category:
    """
    managing categories
    """

    def __init__(self, name, count, url, url_id):
        self.name = name
        self.count = count
        self.url = url
        self.url_id = url_id

    @staticmethod
    def importing():
        """
        used for the 30 biggest categories importing on database
        """
        data = Data('https://fr.openfoodfacts.org/categories.json')
        all_categories = data.load()
        most_important_categories = data.filter(all_categories)
        for category in most_important_categories:
            Category(category['name'],
                     category['products'],
                     category['url'],
                     category['id']).save()

    def save(self):
        """
        method for inserting data into mysql database
        """
        cur = Database.createCursor()
        sql = """ INSERT INTO
            categories (name, count, url, url_id)
            VALUES (%s, %s, %s, %s) """
        val = (self.name, self.count, self.url, self.url_id)
        cur.execute(sql, val)
        Database.databaseConnection.commit()
        print(cur.rowcount, "record inserted.")

    @staticmethod
    def load():
        """
        used to load categories on a dict
        """
        categories = Database().load('categories')
        i = 1
        categories_dict = dict()
        for category in categories:
            categories_dict[i] = category
            i += 1
        return categories_dict

    @staticmethod
    def listing():
        """
        display categories on a bulleted list
        """
        for key, value in Category.load().items():
            print('{} - {}'.format(key, value[1]))

    @staticmethod
    def load_from_id(product_id):
        """
        find categories from a product id
        """
        cur = Database.createCursor()
        cur.execute("""select name from categories
        inner join categories_products
        on categories.id = categories_products.category_id
        where product_id = %s""", (product_id, ))
        return [''.join(x) for x in cur.fetchall()]
