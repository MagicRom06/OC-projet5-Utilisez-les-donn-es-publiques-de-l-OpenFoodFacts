from category import Category
from data import Data


def import_categories_on_db():
    data = Data('https://fr.openfoodfacts.org/categories.json')
    all_categories = data.all()
    most_important_categories = data.filter(all_categories)
    for category in most_important_categories:
        Category(category['name'], category['products'], category['url'], category['id']).save()


def main():
    import_categories_on_db()


if __name__ == '__main__':
    main()
