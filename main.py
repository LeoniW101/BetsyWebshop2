__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import os
from models import *
from datetime import datetime
from populate_test_database import populate_test_database


def main():
  # Set the file name
  database_filename = "betsywebshop.db"

  # Combine current working directory and file name
  database_path = os.path.join(os.getcwd(), database_filename)

  # Check if the database file exists
  if not os.path.exists(database_path):
    # Database does not exist, run database initialization
    populate_test_database()

  # Connect to the database
  Product._meta.database.init(database_path)
  Product._meta.database.connect()

  try:
    # Create tables if they don't exist
    Product._meta.database.create_tables(
        [User, Product, Tag, ProductTag, ProductOwner, PurchaseTransaction],
        safe=True)

    ### Uncomment the following lines for testing purposes to print the contents of the Producttable ####
    #products_in_database = Product.select()
    #for product in products_in_database:
    #  print(
    #      f"Product ID: {product.id}, Name: {product.name}, Description: {product.description}, Price: {product.price}, Quantity: {product.quantity}"
    #  )

    ##########
    # Search for products based on a term.
    def search(term):
      term = term.lower()
      found_products = {}

      query = Product.select().where(Product.name.contains(term))

      for product in query:
        if product.name not in found_products:
          found_products[product.name] = product.quantity
          print(
              f'\n  We have found {product.quantity}x of "{term}" for sale!  ')

      if not found_products:
        print(
            f'\n  We don\'t have any products such as "{term}" for sale, please try again.'
        )

    ##########
    # View the products of a given user.
    def list_user_products(user_id):
      try:
        user_query = User.get(User.id == user_id)
        username = user_query.username

        product_query = (Product.select(
            Product, Product.quantity).join(ProductOwner).where(
                ProductOwner.owner == user_query).order_by(Product.name))

        if product_query:
          print(f'User "{username}" has the following products for sale:')

          for product in product_query:
            print(f'   {product.quantity}x of "{product.name}"  ')

        else:
          print(f'\n  User "{username}" has no products for sale listed. ')

      except User.DoesNotExist:
        print(f'\n  User with ID {user_id} does not exist, please try again. ')

    ########
    # View all products for a given tag.
    def list_products_per_tag(tag_id):
      product_query = (Product.select().join(ProductTag).join(Tag).where(
          ProductTag.tag == tag_id))
      tag_query = Tag.select().where(Tag.id == tag_id).get()
      tagname = tag_query.name

      unique_products = set()

      if product_query:
        print(f'\n  Products with tag: "{tagname}": ')
        for product in product_query:
          if product.name not in unique_products:
            unique_products.add(product.name)
            print(f'   "{product.name}" ')

    #############
    # Add a product to a user.
    def add_product_to_user(user_id, product_info):
      try:
        # Check if the user exists
        user_query = User.get(User.id == user_id)

        # Check if the product exists
        if isinstance(product_info, dict) and "id" in product_info:
          # Add an existing product to the user (this part may vary based on your requirements)
          product_id = product_info["id"]
          product_query = Product.get(Product.id == product_id)
        else:
          # Extract the owner information from product_info
          owner_info = product_info.pop("owner", None)

          # Create a new product and set the user as the owner
          product_query = Product.create(owner=user_query.id, **product_info)

        # Get product and user details
        product_name = product_query.name
        username = user_query.username

        # Print success message
        print(f'\n  "{product_name}" is added to "{username}"!')
      except User.DoesNotExist:
        print(f'\n  Error: User with ID {user_id} does not exist.')
      except Product.DoesNotExist:
        print(
            f'\n  Error: Product with ID {product_info.get("id")} does not exist.'
        )

    ########
    # Update the stock quantity of a product.
    def update_stock(product_id, add_quantity):
      query = Product.select().where(Product.id == product_id).get()
      previous_quantity = query.quantity
      query.quantity = previous_quantity + add_quantity
      query.save()
      if query:
        print(
            f'\n  Updated stock for "{query.name}" with "{add_quantity}" pieces. New stock count is: "{query.quantity}" '
        )

    #########
    # Remove a product from a user.
    def remove_product(product_id, quantity):
      try:
        product_query = Product.get(Product.id == product_id)

        if quantity > product_query.quantity:
          print(
              f"Error: Not enough stock available for product with ID {product_id}."
          )
        else:
          updated_quantity = product_query.quantity - quantity
          product_query.quantity = updated_quantity
          product_query.save()
          print(
              f"Successfully removed {quantity} pieces of {product_query.name}. Updated stock: {updated_quantity}"
          )
      except Product.DoesNotExist:
        print(f"Error: Product with ID {product_id} does not exist.")

    ##############
    # Handle a purchase between a buyer and a seller for a given product
    def purchase_product(product_id, buyer_id, quantity):
      product_query = Product.select().where(Product.id == product_id).get()
      buyer_query = User.select().where(User.id == buyer_id).get()
      if quantity >= product_query.quantity:
        print(
            f'\n  Not enough of "{product_query.name}" on stock for transaction. Please enter new quantity less than "{product_query.quantity}" '
        )
        return

      total_price = round(product_query.price * quantity, 2)

      transactions = PurchaseTransaction.create(
          buyer=buyer_query.id,
          product_bought=product_query.id,
          qty_bought=quantity,
          total_price=total_price,
          date_bought=datetime.now())

      new_quantity = product_query.quantity - quantity
      update_stock(product_query.id, new_quantity)

      print(
          f'\n  "{buyer_query.username}" bought "{transactions.qty_bought}" pieces of "{product_query.name}" '
      )
      print("=" * 40)
      print(f'''ORDER TRANSACTION

    \tPRODUCT:{product_query.name}
    \tQUANTITY:{transactions.qty_bought}

    \tPRICE:{transactions.total_price}

    DATE:{str(transactions.date_bought)}''')
      print("=" * 40)


# 1 Test search function

#    print("\nSearch for 'necklace':")
#    search("necklace")

#    print("\nSearch for 'book':")
#    search("book")

# 2 Test list_user_products function

#    print("\nList products for user with ID 2:")
#    list_user_products(2)

# 3 Test list_products_per_tag function

#    print("\nList products for tag with ID 3:")
#    list_products_per_tag(3)

# 4a Test add_product_to_user function

#    print("\nAdd existing product with ID 3 to existing user with ID 1:")
#    add_product_to_user(1, {"id": 3})

# 4b Test add new product to existing user

#    print("\nAdd new product to existing user with ID 2:")
#    add_product_to_user(
#        2, {
#            "name": "New Product",
#            "description": "Brand new product",
#            "price": 49.99,
#            "quantity": 10,
#        })

# 5 Test update_stock function
#    print("\nUpdate stock for product with ID 1 (add 5):")
#    update_stock(1, 5)

# 6 Test remove_product function
#    print("\nRemove 5 pieces of product with ID 1:")
#    remove_product(1, 5)

# 7 Test purchase_product function

#    print("\nPurchase 1 piece of product with ID 5 by user with ID 2:")
#    purchase_product(5, 2, 1)

  finally:
    # Close the database connection when done
    Product._meta.database.close()

if __name__ == "__main__":
  main()
