from connect import Database
from category import Category
from product import Product


class InterfaceUser:
    def __init__(self):
        self.products = dict()

    def find_substitute(self):
        print('Sélectionnez la catégorie:')
        # affichage des categories
        Category.display_list()
        category_user = input(':')
        for id, category in Category.load().items():
            if int(category_user) == id:

                # on charge et affiche les produits de la catégorie choisie
                self.products = Product.load(category[0])
                Product.display_list(self.products)
                user = input(':')
                for product in self.products:
                    if int(user) == product['id']:
                        Product(product['product'][0][0][6],
                                product['product'][0][0][1],
                                product['product'][0][0][2],
                                product['product'][0][0][3],
                                product['product'][0][0][5],
                                product['product'][0][0][4],
                                product['product'][2],
                                product['product'][1]).display_one()

    def play(self):
        Database.connect()
        user = input("""1 - Quel aliment souhaitez-vous remplacer ?
        2 - Retrouver mes aliments substitués.
        3 - Quitter
        :""")
        try:
            user = int(user)
        except:
            return self.play()
        else:
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
