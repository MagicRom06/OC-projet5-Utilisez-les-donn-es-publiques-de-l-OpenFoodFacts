from connect import Database


class Store:
    """
    Used for importing stores
    """
    def __init__(self, name):
        self.name = name

    def save(self):
        """
        Used for inserting stores on database
        """
        db = Database()
        cnx = db.connect()
        cur = cnx.cursor()
        sql = """ INSERT INTO stores (name) VALUES (%s) """
        val = (self.name, )
        cur.execute(sql, val)
        cnx.commit()
        print(cur.rowcount, "record inserted.")
