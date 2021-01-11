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
        db = Database()
        cnx = db.connect()
        cur = cnx.cursor()
        sql = """ INSERT INTO
            categories (name, count, url, url_id)
            VALUES (%s, %s, %s, %s) """
        val = (self.name, self.count, self.url, self.url_id)
        cur.execute(sql, val)
        cnx.commit()
        print(cur.rowcount, "record inserted.")
