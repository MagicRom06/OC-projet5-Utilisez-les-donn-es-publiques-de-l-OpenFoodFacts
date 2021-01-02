from data import Data


class Product:
    def __init__(self):
        self.url = 'https://fr.openfoodfacts.org/stores.json'

    def save(self):
        stores = Data(self.url).all()
