from category import Category
from connect import Database
from product import Product
from substitute import Substitute


class InterfaceUser:
    """
    used for display user choices
    """
    def __init__(self):
        self.user_product = None

    def find_substitute(self):
        """
        used for finding a substitute from a product selected by the user
        """
        print('Sélectionnez la catégorie:')
        Category.listing()
        category_user = input(':')
        try:
            category_user = int(category_user)
            assert 0 < category_user <= len(Category.load())
        except ValueError:
            return self.find_substitute()
        except AssertionError:
            return self.find_substitute()

        # load product from the chosen category
        for id, category in Category.load().items():
            if int(category_user) == id:

                # load and display products
                products = Product.load(category[0])
                print('Sélectionnez un produit:')
                Product.listing(products)
                product_user = input(':')
                try:
                    product_user = int(product_user)
                    assert 0 < product_user <= len(products) + 1
                except ValueError:
                    self.find_substitute()
                except AssertionError:
                    self.find_substitute()

                for product in products:
                    if product_user == product['id']:
                        self.user_product = product['product']
                        product['product'].display()
                substitute = Substitute(self.user_product).find()
                print(substitute)

    def play(self):
        """
        main method
        """
        Database.connect()
        user = input("""1 - Quel aliment souhaitez-vous remplacer ?
2 - Retrouver mes aliments substitués.
3 - Quitter
:""")
        try:
            user = int(user)
            assert 0 < user <= 3
        except ValueError:
            return self.play()
        except AssertionError:
            return self.play()
        if user == 1:
            self.find_substitute()
            Database.disconnect()
        elif user == 2:
            print(user)
        elif user == 3:
            print('You\'re leaving the programm')
            Database.disconnect()
            exit()
        else:
            print('Choice has to be 1, 2 or 3')
            return self.play()
