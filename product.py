from connect import Database


class Product:
    def __init__(self, brands, name, image, url, description, nutriscore, stores, categories):
        self.brands = brands
        self.name = name
        self.image = image
        self.url = url
        self.description = description
        self.nutriscore = nutriscore
        self.stores = stores
        self.categories = categories

    def save(self):
        db = Database()
        cnx = db.connect()
        cur = cnx.cursor()
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
        cnx.commit()

        if len(self.stores) > 0 and "intermarchė" not in self.stores:
            print(self.stores)
            for elt in self.stores:
                if elt != "intermarche":
                    print(elt)
                    cur.execute("select id from stores where name = %s", (str(elt), ))
                    id = cur.fetchone()[0]
                    print(id, last_product_id)
                    sql = """INSERT INTO store_product (store_id, product_id) VALUES (%s, %s)"""
                    cur.execute(sql, (int(id), int(last_product_id)))
                    cnx.commit()
