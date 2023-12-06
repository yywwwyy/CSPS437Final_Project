# Import necessary libraries
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import csv

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Define your database models here
class Restaurant(db.Model):
    restaurant_id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100))
    score = db.Column(db.Numeric(2, 1))
    price_range = db.Column(db.Integer)
    street = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip = db.Column(db.String(50))

class restaurant_category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer)
    category_type = db.Column(db.String(100))

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer)
    category_type = db.Column(db.String(100))
    name = db.Column(db.String(100))
    price = db.Column(db.String(50))

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer)

def insert_restaurant_data(restaurant_path):
    with open(restaurant_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Create a new restaurant instance for each row in the CSV
            score = float(row['Score']) if row['Score'] and row['Score'] != 'None' else None
            price_range = float(row['Price_range']) if row['Price_range'] and row['Price_range'] != 'None' else None
            zipint = int(row['Zip'])
            restaurant = Restaurant(
                restaurant_id=row['Restaurant_id'],
                restaurant_name=row['Restaurant_name'],
                score=score,
                price_range=price_range,
                street=row['Street'],
                city=row['City'],
                state=row['State'],
                zip=zipint,
            )
            # Add the Student instance to the session
            db.session.add(restaurant)
        db.session.commit()



# insert csv data to db
def insert_restaurant_category_data(categories_path):
    with open(categories_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Create a new restaurant instance for each row in the CSV
            rest_cat = restaurant_category(
                restaurant_id=row['Restaurant_id'],
                category_type=row['Category_type'],
            )
            # Add the Student instance to the session
            db.session.add(rest_cat)
        db.session.commit()


# insert csv data to db
def insert_dish_data(restaurant_menus_path):
    with open(restaurant_menus_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Create a new restaurant instance for each row in the CSV
            dish = Dish(
                restaurant_id=row['restaurant_id'],
                category_type=row['category'],
                name=row['name'],
                price=row['price'],
            )
            # Add the Student instance to the session
            db.session.add(dish)
        db.session.commit()


# Function to initialize the database
def initialize_database():
    # csv paths
 #   restaurant_path = 'CSV_DATA/restaurant_dataset.csv'
    restaurant_path_new = 'CSV_DATA/restaurant_data_new.csv'
    restaurant_menus_path = 'CSV_DATA/restaurant_menus.csv'
    categories_path = 'CSV_DATA/categories.csv'
    # test path
#   restaurant_short_path = 'CSV_DATA/restaurant_short.csv'
#   categories_short_path = 'CSV_DATA/categories_short.csv'
#   restaurant_menus_short_path = 'CSV_DATA/restaurant_menus_short.csv'
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_restaurant_data(restaurant_path_new)
        insert_restaurant_category_data(categories_path)
        insert_dish_data(restaurant_menus_path)

if __name__ == '__main__':
    # Initialize the database
    initialize_database()
