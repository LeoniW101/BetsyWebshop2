from peewee import *

db = SqliteDatabase("betsywebshop.db")


class BaseModel(Model):

  class Meta:
    database = db


class User(BaseModel):
  username = CharField()
  first_name = CharField()
  last_name = CharField()
  street = CharField()
  house_number = CharField()
  postal_code = CharField()
  city = CharField()
  email = CharField()
  payment_method = CharField()


class Product(BaseModel):
  name = CharField()
  description = TextField()
  price = DecimalField(decimal_places=2, auto_round=True)
  quantity = IntegerField()
  owner = DeferredForeignKey('ProductOwner', backref='products')


class ProductOwner(BaseModel):
  product = ForeignKeyField(Product)
  owner = ForeignKeyField(User)


class Tag(BaseModel):
  name = CharField(unique=True)


class ProductTag(BaseModel):
  product = ForeignKeyField(Product)
  tag = ForeignKeyField(Tag)


class PurchaseTransaction(BaseModel):
  buyer = ForeignKeyField(User)
  product_bought = ForeignKeyField(Product)
  qty_bought = IntegerField()
  total_price = DecimalField(decimal_places=2, auto_round=True)
  date_bought = DateTimeField(formats='%d-%m-%Y')
