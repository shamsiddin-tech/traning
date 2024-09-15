# numbers = [10, 498, 45, 5, 6, 8, 1]
#
# def even_numbers(numbers:int):
#     return numbers % 2 == 0
#     return numbers.sorted(reversed)
#
# even = filter(even_numbers, numbers)
# sorted = sorted(even, reverse=True)
# print(sorted)



# def factorial(number):
#     length = 1
#     for i in range(1, number+1):
#         length *= i
#     return length
#
# check = factorial(4)
# print(check)







# class Product:
#     def __init__(self, name, price):
#         self.name = name
#         self.price = price
#
# class Order(Product):
#     def all_products(self):
#         self.name = Product.name
#         self.price = Product.price
#         return f'продукты:\n{self.name} -> {self.price}'
#
#
# class Customer(Order):
#     def __init__(self, name, product):
#         super().__init__(name, product)
#         self.name = name
#         self.product = product
#     def have_bought(self):
#         return f'{self.name} купил {self.product} цена:{self.price}'
#
# product1 = Product(name='телефон', price=1000)
# product2 = Product(name='комп', price=10000)
# product3 = Product(name='машина', price=30000)
#
# customer1 = Customer('shams', product3)
# customer2 = Customer('nuri', product2)
# customer3 = Customer('sam', product1)
#
# print(f'был куплен товар: {customer1.product.price} за {customer1.product.name}\n'
#       f'был куплен товар: {customer2.product.name} за {customer2.product.price}\n'
#       f'был куплен товар: {customer3.product.name} за {customer3.product.price}')








# class Bank:
#     balance = 0
#     def _add_money(self, amount):
#         self.amount = amount
#         self.balance += amount
#         return f'вы добавили; {self.amount}'
#     def _withdraw(self, amount):
#         self.amount = amount
#         self.balance -= self.amount
#         return f'вы сняли {self.amount}'
#     def show_balance(self):
#         return f'ваш баланс -> {self.balance}'
#
#
# add = int(input('добавьте сумму: '))
# minus = int(input('выведите сумму: '))
# mybank = Bank()
# print(mybank._add_money(add))
# print(mybank._withdraw(minus))
# print(mybank.show_balance())



# class Figures:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     def perimetr(self):
#         return f'периметр а и б =={2 *(self.a + self.b)}'
#     def ploshad(self):
#         return f'площадь == {self.a * self.b}'
#
# figures = Figures()





# from sqlalchemy import Column, create_engine, INTEGER, ForeignKey, Text, Date, String
# from sqlalchemy.orm import declarative_base, sessionmaker
#
# Base = declarative_base()
#
# class User(Base):
#     __tablename__ = 'user'
#
#     uid = Column('id', INTEGER, primary_key=True)
#     user_name = Column('user_name', String)
#
#     def __init__(self, user_name):
#         self.user_name = user_name
#
# class Post(Base):
#     __tablename__ = 'post'
#
#     pid = Column('id', INTEGER, primary_key=True)
#     title = Column('title', Text)
#     posted_date = Column('posted_date', Date)
#     user_id = Column('whom_posted', INTEGER, ForeignKey('user.id'))
#
#     def __init__(self, title, posted_date, user_id):
#         self.title = title
#         self.posted_date = posted_date
#         self.user_id = user_id
#
# class Comment(Base):
#     __tablename__ = 'comment'
#
#     cid = Column('id', INTEGER, primary_key=True)
#     comment = Column('comment', Text)
#     user_id_com = Column('whom_commented', INTEGER, ForeignKey('user.id'))
#
#     def __init__(self, comment, user_id_com):
#         self.comment = comment
#         self.user_id_com = user_id_com
#
# engine = create_engine('postgresql://postgres:123456@localhost/overall_traning', echo=True)
# Base.metadata.create_all(bind=engine)
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Add users
# u1 = User('shams')
# u2 = User('nuri')
# u3 = User('doni')
#
# session.add_all([u1, u2, u3])
# session.commit()  # Commit to make sure users are in the database
#
# # Get user IDs to use in Post and Comment
# u1_id = session.query(User).filter_by(user_name='shams').first().uid
# u2_id = session.query(User).filter_by(user_name='nuri').first().uid
#
# # Add posts
# p1 = Post('today was great day', '2024-09-14', u1_id)
# p2 = Post('yestarday also was not bad', '2024-09-13', u1_id)
# p3 = Post('tomorrow I will complete my traning', '2024-09-15', u2_id)
#
# session.add_all([p1, p2, p3])
# session.commit()
#
# # Add comments
# c1 = Comment('I will move to US', u1_id)
# c2 = Comment('I will be programist', u1_id)
# c3 = Comment('I really like coffee', u2_id)
#
# session.add_all([c1, c2, c3])
# session.commit()



from tortoise import Tortoise, models, fields, run_async


class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)

    class Meta:
        table = 'category'

class Product(models.Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    price = fields.IntField()
    category = fields.ForeignKeyField('models.Category', related_name='categories')

    class Meta:
        table = 'product'

class Order(models.Model):
    id = fields.IntField(primary_key=True)
    product = fields.ForeignKeyField('models.Product', related_name='products')
    quantity = fields.IntField()

    class Meta:
        table = 'orders'

async def main():
    await Tortoise.init(
        db_url='postgres://postgres:123456@localhost/tortoise_traning',
        modules={"models": ['__main__']}
    )
    await Tortoise.generate_schemas()


    result = Category.bulk_create([
        Category(name='электроника'),
        Category(name='машины')
    ])
    print(f'{result}')



    result2 = Product.bulk_create([
        Product(name='микроволновка', price='500', category_id=1),
        Product(name='телефон', price='200', category_id=1),
        Product(name='бмв', price='5000', category_id=2),
        Product(name='spark', price='1500', category_id=2),
        Product(name='bentley', price='10000', category_id=2)
    ])
    print(f'{result2}')

if __name__ == '__main__':
    run_async(main())