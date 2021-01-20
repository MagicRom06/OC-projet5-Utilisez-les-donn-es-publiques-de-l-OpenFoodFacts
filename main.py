from category import Category
from connect import Database
from data import Data
from product import Product
from store import Store
from interface_user import InterfaceUser


def import_categories_on_db():
    """
    used for the 30 biggest categories importing on database
    """
    data = Data('https://fr.openfoodfacts.org/categories.json')
    all_categories = data.all()
    most_important_categories = data.filter(all_categories)
    for category in most_important_categories:
        Category(category['name'],
                 category['products'],
                 category['url'],
                 category['id']).save()


def import_stores_on_db():
    """
    used for stores importing on database ordered by abc
    """
    store_list = list()
    stores = Data('https://fr.openfoodfacts.org/stores.json').all()
    for store in stores:
        store_list.append(store['id'])
    store_list = sorted(store_list)
    for elt in store_list:
        Store(elt).save()


def import_products_on_db():
    """
    used for products importing on database
    """
    categories = Database().load('categories')
    for category in categories:
        products = Data(category[3] + '.json').all()
        for product in products:
            if 'stores' in product.keys() \
                    and 'nutriscore_grade' in product.keys() \
                    and 'ingredients_text_fr' in product.keys() \
                    and 'image_url' in product.keys():
                Product(product['brands'],
                        product['product_name'],
                        product['image_url'],
                        product['url'],
                        product['ingredients_text_fr'],
                        product['nutriscore_grade'],
                        product['stores_tags'],
                        product['categories_tags']).save()


def main():
    InterfaceUser().play()


if __name__ == '__main__':
    main()
