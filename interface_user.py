from connect import Database
from category import Category
from product import Product


class InterfaceUser:
    def __init__(self):
        self.products = list()

    def find_substitute(self):
        print('Sélectionnez la catégorie:')

        # affichage des categories
        Category.display()
        category_user = input(':')
        for id, category in Category.load().items():
            if int(category_user) == id:

                # on charge les produits de la catégorie choisie
                self.products = Product.load(category[0])

                # on affiche la liste
                Product.display(self.products)

                # on ajoute les catégories dans la liste des produits générée
                self.products = Product.add_categories(self.products)
                print(self.products)




                """
                product_user = input(':')

        # Récupération du product_id selon le category_id du choix de l'utilisateur
        for key, value in self.categories_dict.items():
            if int(user) == key:
                cur.execute('select product_id from categories_products where category_id = %s', (value[0],))
                product_id = cur.fetchall()
                i = 1

                # On parcourt les product_id afin de recupérer les produits associés
                for id in product_id:
                    cur.execute('select id, brand, name from products where id = %s', (id[0],))
                    products = cur.fetchall()


                    # On parcourt les produits trouvés que l'ont placent dans un dict
                    # afin de leur attribuer un int en tant que clé
                    for product in products:
                        self.products_dict[i] = product  # Product()
                        i += 1

                # On affiche les produits de la catégorie choisie par l'utilisateur
                for key, value in self.products_dict.items():
                    print('{} - {} - {}'.format(key, value[1], value[2]))

        # L'utilisateur choisi un produit dans la liste
        user = input(':')

        # On récupère le produit choisit dans une liste
        for key, value in self.products_dict.items():
            if int(user) == key:
                cur.execute('select * from products where id = %s', (value[0],))
                product = cur.fetchone()
                for elt in product:
                    self.selected_product.append(elt)

                # On récupère le store_id associé au product_id
                cur.execute('select store_id from stores_products where product_id = %s',
                            (self.selected_product[0],))
                store_id = cur.fetchall()

                # On récupère le store associé au store_id
                stores = list()
                for id in store_id:
                    cur.execute('select * from stores where id = %s', (id[0],))
                    selected_product_store = cur.fetchone()[1]
                    stores.append(selected_product_store)

                # On ajoute le store à la liste du produit
                self.selected_product.append(stores)

        # On répète le même processus de récupération du store avec les catégories
        cur.execute("select category_id from categories_products where product_id = %s",
                    (self.selected_product[0],))
        category_id = cur.fetchall()
        categories = list()
        for id in category_id:
            cur.execute('select name from categories where id = %s', (id[0],))
            selected_product_categories = cur.fetchone()[0]
            categories.append(selected_product_categories)
        self.selected_product.append(categories)

        # Affichage du produit choisi par l'utilisateur
        print("***********\nid : {}\n"
              "Marque : {}\n"
              "Nom du produit : {}\n"
              "Url : {}\n"
              "Image : {}\n"
              "Nutriscore : {}\n"
              "Magasins : {}\n"
              "Catégories : {}\n"
              "Description : {}\n***********".format(self.selected_product[0],
                                                     self.selected_product[6],
                                                     self.selected_product[1],
                                                     self.selected_product[3],
                                                     self.selected_product[2],
                                                     self.selected_product[4],
                                                     ', '.join(self.selected_product[7]),
                                                     ', '.join(self.selected_product[8]),
                                                     self.selected_product[5])) """

    def play(self):
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
            elif user == 2:
                print(user)
            elif user == 3:
                print('You\'re leaving the programm')
                exit()
            else:
                print('Choice has to be 1, 2 or 3')
                return self.play()
