from connect import Database


class Store:
    def __init__(self, name):
        self.name = name

    def save(self):
        db = Database()
        cnx = db.connect()
        cur = cnx.cursor()
        sql = """ INSERT INTO stores (name) VALUES (%s) """
        val = (self.name, )
        cur.execute(sql, val)
        cnx.commit()
        print(cur.rowcount, "record inserted.")
