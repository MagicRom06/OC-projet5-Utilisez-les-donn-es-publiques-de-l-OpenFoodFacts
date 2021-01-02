from category import Category
from data import Data
from connect import Database
from store import Store


def import_categories_on_db():
    data = Data('https://fr.openfoodfacts.org/categories.json')
    all_categories = data.all()
    most_important_categories = data.filter(all_categories)
    for category in most_important_categories:
        Category(category['name'],
                 category['products'],
                 category['url'],
                 category['id']).save()


def import_stores_on_db():
    store_list = list()
    stores = Data('https://fr.openfoodfacts.org/stores.json').all()
    for store in stores:
        store_list.append(store['name'])
    store_list = sorted(store_list)
    for elt in store_list:
        Store(elt).save()


def main():
    """
    db = Database()
    cnx = db.connect()
    cur = cnx.cursor()
    cur.execute(" SELECT * from categories")
    categories = cur.fetchall()
    print(categories)
    """
    import_stores_on_db()


if __name__ == '__main__':
    main()
