from connect import Database


class Category:
    """
    Class used to get categories data from openfoodfacts data,
    and insert it to mysql database
    """

    def __init__(self, name, count, url, url_id):
        self.name = name
        self.count = count
        self.url = url
        self.url_id = url_id

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
        categories = Database().load('categories')
        i = 1
        categories_dict = dict()
        for category in categories:
            categories_dict[i] = category
            i += 1
        return categories_dict

    @staticmethod
    def display_list():
        for key, value in Category.load().items():
            print('{} - {}'.format(key, value[1]))
