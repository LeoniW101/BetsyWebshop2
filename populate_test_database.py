# populate_test_database.py
from datetime import datetime
from models import *


def create_tables():
  with db:
    db.create_tables(
        [User, Product, Tag, ProductTag, ProductOwner, PurchaseTransaction])


def populate_test_database():

  create_tables()

  users = [
      {
          "username": "Terry555",
          "first_name": "Teresa",
          "last_name": "Smith",
          "street": "Terrystreet",
          "house_number": "555",
          "postal_code": "1234AB",
          "city": "Cityville",
          "email": "terry@example.com",
          "payment_method": "card"
      },
      {
          "username": "John123",
          "first_name": "Jonathan",
          "last_name": "Doe",
          "street": "Johnstreet",
          "house_number": "123",
          "postal_code": "9012EF",
          "city": "Villageville",
          "email": "john@example.com",
          "payment_method": "card"
      },
      {
          "username": "Erica987",
          "first_name": "Eleanor",
          "last_name": "Johnson",
          "street": "Ericastreet",
          "house_number": "987",
          "postal_code": "3456GH",
          "city": "Hamletsville",
          "email": "erica@example.com",
          "payment_method": "bitcoins"
      },
      {
          "username": "Alice123",
          "first_name": "Alice",
          "last_name": "Miller",
          "street": "Wonderland",
          "house_number": "456",
          "postal_code": "6789IJ",
          "city": "Fantasy City",
          "email": "alice@example.com",
          "payment_method": "card"
      },
      {
          "username": "Bob456",
          "first_name": "Bob",
          "last_name": "Johnson",
          "street": "Mainstreet",
          "house_number": "789",
          "postal_code": "1234KL",
          "city": "Smalltown",
          "email": "bob@example.com",
          "payment_method": "bitcoins"
      },
      {
          "username": "Graham789",
          "first_name": "Greta",
          "last_name": "Jones",
          "street": "Grahamstreet",
          "house_number": "789",
          "postal_code": "5678CD",
          "city": "Townsville",
          "email": "graham@example.com",
          "payment_method": "bitcoins"
      },
  ]

  for user_data in users:
    User.create(**user_data)

  products = [
      {
          "name": "Handcrafted Silver Necklace",
          "description": "Elegant silver necklace, meticulously handcrafted",
          "price": 90.00,
          "quantity": 25,
          "owner": User.get(User.username == "Erica987").id
      },
      {
          "name": "Artisan Gemstone Earrings",
          "description":
          "Unique gemstone earrings with intricate artisan detailing",
          "price": 65.00,
          "quantity": 40,
          "owner": User.get(User.username == "John123").id
      },
      {
          "name": "Vintage-Inspired Wall Art",
          "description": "Charming wall art with a touch of vintage elegance",
          "price": 85.00,
          "quantity": 20,
          "owner": User.get(User.username == "Graham789").id
      },
      {
          "name": "Boho Printed Dress",
          "description": "Bohemian-style printed dress for women",
          "price": 25.00,
          "quantity": 175,
          "owner": User.get(User.username == "Terry555").id
      },
      {
          "name": "Hand-Painted White Sneakers",
          "description":
          "Customized white sneakers with unique hand-painted designs",
          "price": 155.00,
          "quantity": 200,
          "owner": User.get(User.username == "Bob456").id
      },
      {
          "name": "Elegant Ceramic Vase Set",
          "description":
          "Set of two elegant ceramic vases for stylish home decor",
          "price": 45.00,
          "quantity": 50,
          "owner": User.get(User.username == "Alice123").id
      },
  ]

  for product_data in products:
    Product.create(**product_data)

  tags = [{"name": "clothing"}, {"name": "jewelry"}, {"name": "home decor"}]

  for tag_data in tags:
    Tag.create(**tag_data)

  product_tags = [
      {
          "product":
          Product.get(Product.name == "Handcrafted Silver Necklace"),
          "tag": Tag.get(Tag.name == "jewelry")
      },
      {
          "product": Product.get(Product.name == "Artisan Gemstone Earrings"),
          "tag": Tag.get(Tag.name == "jewelry")
      },
      {
          "product": Product.get(Product.name == "Vintage-Inspired Wall Art"),
          "tag": Tag.get(Tag.name == "home decor")
      },
      {
          "product": Product.get(Product.name == "Boho Printed Dress"),
          "tag": Tag.get(Tag.name == "clothing")
      },
      {
          "product":
          Product.get(Product.name == "Hand-Painted White Sneakers"),
          "tag": Tag.get(Tag.name == "clothing")
      },
      {
          "product": Product.get(Product.name == "Elegant Ceramic Vase Set"),
          "tag": Tag.get(Tag.name == "home decor")
      },
  ]

  for product_tag_data in product_tags:
    ProductTag.create(**product_tag_data)

  product_owners = [
      {
          "owner": User.get(User.username == "Erica987"),
          "product":
          Product.get(Product.name == "Handcrafted Silver Necklace"),
          "quantity": 20
      },
      {
          "owner": User.get(User.username == "John123"),
          "product": Product.get(Product.name == "Artisan Gemstone Earrings"),
          "quantity": 45
      },
      {
          "owner": User.get(User.username == "Graham789"),
          "product":
          Product.get(Product.name == "Hand-Painted White Sneakers"),
          "quantity": 68
      },
      {
          "owner": User.get(User.username == "Terry555"),
          "product": Product.get(Product.name == "Elegant Ceramic Vase Set"),
          "quantity": 87
      },
      {
          "owner": User.get(User.username == "Bob456"),
          "product": Product.get(Product.name == "Vintage-Inspired Wall Art"),
          "quantity": 36
      },
      {
          "owner": User.get(User.username == "Alice123"),
          "product": Product.get(Product.name == "Boho Printed Dress"),
          "quantity": 50
      },
  ]

  for product_owner_data in product_owners:
    ProductOwner.create(owner=product_owner_data["owner"],
                        product=product_owner_data["product"],
                        quantity=product_owner_data["quantity"])


if __name__ == "__main__":
  populate_test_database()
