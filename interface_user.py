from category import Category
from connect import Database
from product import Product
from substitute import Substitute
from store import Store


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

        # display categories
        Category.listing()

        # ask the user to choose a category
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
                products = Product.load(category.id)
                print('Sélectionnez un produit:')
                Product.listing(products)

                # ask the user to choose a product
                product_user = input(':')
                try:
                    product_user = int(product_user)
                    assert 0 < product_user <= len(products) + 1
                except ValueError:
                    self.find_substitute()
                except AssertionError:
                    self.find_substitute()

                # display the chosen product
                for product in products:
                    if product_user == product['id']:
                        self.user_product = product['product']
                        print(product['product'].display())

                # find 5 max substituts from the chosen product
                substituts = Substitute.find(self.user_product)

                # check if there is no substituts for the chosen product
                if len(substituts) == 0:
                    print('Aucun substitut trouvé')
                    # if yes the user is redirected to the main menu
                    return self.play()
                else:
                    # if not, substituts are displayed
                    Substitute.listing(substituts)

                    # ask the user if he wants to save a substitut
                    # if not, the user is redirected to the main menu
                    # if yes he has to choose a substitut
                    if self.save_substitute():
                        substitut_user = input(
                            'Veuillez indiquer le chiffre correspondant au produit\n:')
                        try:
                            substitut_user = int(substitut_user)
                            assert 0 < substitut_user <= len(substituts)
                        except ValueError:
                            print('erreur valeur')
                            return self.find_substitute()
                        except AssertionError:
                            print('erreur assertion')
                            return self.find_substitute()

                        # save the chosen substitut
                        # back to the main menu
                        for product in substituts:
                            if substitut_user == product['id']:
                                Substitute(product['product'].id,
                                           self.user_product.id).save()
                                print('Produit sauvegardé')
                                self.play()

    def play(self):
        """
        main method
        """
        Database.connect()
        if Database().is_empty():
            Category.importing()
            Store.importing()
            Product.importing()
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
            products = Substitute.load()
            for product in products:
                print(Product.get(product[0]).display())
            self.play()
        elif user == 3:
            print('You\'re leaving the programm')
            Database.disconnect()
            exit()
        else:
            print('Choice has to be 1, 2 or 3')
            return self.play()

    def save_substitute(self):
        """
        ask the user if he wants
        to save or not a substitute
        """
        user = input('Voulez-vous enregistrer un substitut ? o/n\n:')
        try:
            assert user == 'o' or user == 'n'
        except AssertionError:
            print("La réponse doit être 'o' ou 'n'")
            return self.save_substitute()
        if user == 'n':
            return self.play()
        if user == 'o':
            return True
