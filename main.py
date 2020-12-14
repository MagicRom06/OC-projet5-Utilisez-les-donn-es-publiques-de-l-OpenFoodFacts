from category import Category

categories_data = Category()
data = categories_data.filtered_data(categories_data.get_all_data())
categories_data.insert_to_db(data)
