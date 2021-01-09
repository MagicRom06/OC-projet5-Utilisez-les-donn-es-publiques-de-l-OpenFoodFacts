from category import Category
from data import Data
from connect import Database
from store import Store
from product import Product


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


def import_products_on_db():
    data = list()
    categories = Database().load('categories')
    for category in categories:
        products = Data(category[3] + '.json').all()
        for product in products:
            if 'stores' in product.keys() and 'nutriscore_grade' in product.keys() and 'ingredients_text_fr' in product.keys() and 'image_url' in product.keys():
                data.append({'brands': product['brands'],
                             'name': product['product_name'],
                             'image': product['image_url'],
                             'url': product['url'],
                             'description': product['ingredients_text_fr'],
                             'nutriscore': product['nutriscore_grade'],
                             'stores': product['stores'],
                             'categories': product['categories']})

    for elt in data:
        Product(elt['brands'],
                elt['name'],
                elt['image'],
                elt['url'],
                elt['description'],
                elt['nutriscore'],
                elt['stores'].split(',')[0],
                elt['categories'].split(',')[0]).save()


def main():
    import_categories_on_db()
    import_products_on_db()
    Database().delete_null_entries()


if __name__ == '__main__':
    main()
