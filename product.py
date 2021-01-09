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
        nutriscore,
        stores,
        categories) 
        VALUES (%s, %s, %s, %s, %s, %s, 
        (SELECT id FROM stores WHERE name = %s LIMIT 1), 
        (SELECT id FROM categories WHERE name = %s LIMIT 1)) """
        val = (self.brands,
               self.name,
               self.image,
               self.url,
               self.description,
               self.nutriscore,
               self.stores,
               self.categories)
        cur.execute(sql, val)
        print('execution requête sql')
        cnx.commit()
        print(cur.rowcount, "record inserted.")
