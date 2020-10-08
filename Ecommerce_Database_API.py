#!/usr/bin/env python
# coding: utf-8


####E-commerce####
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from datetime import datetime,timedelta
from sqlalchemy import Table, Column, Integer, ForeignKey
from faker import Faker
import random


####Connect Database####
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://fbvqhnii:PWxxxxxxxxxxx.db.elephantsql.com:5432/fbvqhnii'
db = SQLAlchemy(app)



####Create Table####
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, first_name, last_name, address, city, postcode, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address 
        self.city = city
        self.postcode = postcode
        self.email = email
    


    orders = db.relationship('Order', backref='customer')


order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
    )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    
    def __init__(self, order_date, shipped_date, delivered_date, coupon_code, customer_id):
        self.order_date = order_date
        self.shipped_date = shipped_date
        self.delivered_date = delivered_date
        self.coupon_code = coupon_code
        self.customer_id = customer_id

    products = db.relationship('Product', secondary=order_product)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price


if __name__ == '__main__':
    db.create_all()


####API reguest by postman####
@app.route('/insert_user', methods=['POST'])

def insertUser():
    newFirstName = request.form['first_name']
    newLastName = request.form['last_name']
    newAddress = request.form['address']
    newCity = request.form['city']
    newPostcode = request.form['postcode']
    newEmail = request.form['email']
    
    user = Customer(newFirstName, newLastName, newAddress, newCity, newPostcode, newEmail)
    
    db.session.add(user)
    
    db.session.commit()
    return "<p>Data is updated</p>"



@app.route('/insert_user1', methods=['POST'])

def insertUser1():
    newOrder_date = request.form['order_date']
    newShipped_date = request.form['shipped_date']
    newDelivered_date = request.form['delivered_date']
    newCoupon_code = request.form['coupon_code']
    newCustomer_id = request.form['customer_id']
    
    
    user1 = Order(newOrder_date, newShipped_date, newDelivered_date, newCoupon_code, newCustomer_id)
    db.session.add(user1)
    db.session.commit()
    return "<p>Data is updated</p>"



@app.route('/insert_user2', methods=['POST'])

def insertUser2():
    
    newName = request.form['name']
    newPrice = request.form['price']
         
    user2 = Product(newName, newPrice)    
    db.session.add(user2)
    db.session.commit()
    return "<p>Data is updated</p>"



####Show the address for Postman API####
if __name__ == '__main__':
    app.run()



fake = Faker()



### create random data###
def add_customers():
    for _ in range(100):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.street_address(),
            city=fake.city(),
            postcode=fake.postcode(),
            email=fake.email()
        )
        db.session.add(customer)
db.session.commit()

def add_orders():
    customers = Customer.query.all()

    for _ in range(1000):
        #choose a random customer
        customer = random.choice(customers)

        ordered_date = fake.date_time_this_year()
        shipped_date = random.choices([None, fake.date_time_between(start_date=ordered_date)], [10, 90])[0]

        #choose either random None or random date for delivered and shipped
        delivered_date = None
        if shipped_date:
            delivered_date = random.choices([None, fake.date_time_between(start_date=shipped_date)], [50, 50])[0]

        #choose either random None or one of three coupon codes
        coupon_code = random.choices([None, '50OFF', 'FREESHIPPING', 'BUYONEGETONE'], [80, 5, 5, 5])[0]

        order = Order(
            customer_id=customer.id,
            order_date=ordered_date,
            shipped_date=shipped_date,
            delivered_date=delivered_date,
            coupon_code=coupon_code
        )

        db.session.add(order)
    db.session.commit()

def add_products():
    for _ in range(10):
        product = Product(
            name=fake.color_name(),
            price=random.randint(10,100)
        )
        db.session.add(product)
    db.session.commit()
    
def add_order_products():
    orders = Order.query.all()
    products = Product.query.all()

    for order in orders:
        #select random k
        k = random.randint(1, 3)
        # select random products
        purchased_products = random.sample(products, k)
        order.products.extend(purchased_products)
        
    db.session.commit()

def add_orders():
    customers = Customer.query.all()

    for _ in range(1000):
        #choose a random customer
        customer = random.choice(customers)

        ordered_date = fake.date_time_this_year()
        shipped_date = random.choices([None, fake.date_time_between(start_date=ordered_date)], [10, 90])[0]

        #choose either random None or random date for delivered and shipped
        delivered_date = None
        if shipped_date:
            delivered_date = random.choices([None, fake.date_time_between(start_date=shipped_date)], [50, 50])[0]

        #choose either random None or one of three coupon codes
        coupon_code = random.choices([None, '50OFF', 'FREESHIPPING', 'BUYONEGETONE'], [80, 5, 5, 5])[0]

        order = Order(
            customer_id=customer.id,
            order_date=ordered_date,
            shipped_date=shipped_date,
            delivered_date=delivered_date,
            coupon_code=coupon_code
        )

        db.session.add(order)
    db.session.commit()

def add_products():
    for _ in range(10):
        product = Product(
            name=fake.color_name(),
            price=random.randint(10,100)
        )
        db.session.add(product)
    db.session.commit()
    
def add_order_products():
    orders = Order.query.all()
    products = Product.query.all()

    for order in orders:
        #select random k
        k = random.randint(1, 3)
        # select random products
        purchased_products = random.sample(products, k)
        order.products.extend(purchased_products)
        
    db.session.commit()



def create_random_data():
    db.create_all()
    add_customers()
    add_orders()
    add_products()
    add_order_products()


####Data Analysis####

def get_orders_by(customer_id=1):
    print('Get Orders by Customer')
    customer_orders = Order.query.filter_by(customer_id=customer_id).all()
    for order in customer_orders:
        print(order.order_date)

def get_pending_orders():
    print('Pending Orders')
    pending_orders = Order.query.filter(Order.shipped_date.is_(None)).order_by(Order.order_date.desc()).all()
    for order in pending_orders:
        print(order.order_date)

def how_many_customers():
    print('How many customers?')
    print(Customer.query.count())

def orders_with_code():
    print('Orders with coupon code')
    orders = Order.query.filter(Order.coupon_code.isnot(None)).filter(Order.coupon_code != 'FREESHIPPING').all()
    for order in orders:
        print(order.coupon_code)

def revenue_in_last_x_days(x_days=30):
    print('Revenue past x days')
    print(db.session
        .query(db.func.sum(Product.price))
        .join(order_product).join(Order)
        .filter(Order.order_date > (datetime.now() - timedelta(days=x_days))
        ).scalar()
    )
