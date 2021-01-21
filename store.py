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
        cur = Database.createCursor()
        sql = """ INSERT INTO stores (name) VALUES (%s) """
        val = (self.name, )
        cur.execute(sql, val)
        Database.databaseConnection.commit()
        print(cur.rowcount, "record inserted.")
