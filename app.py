import csv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# Model define (Table Define)

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


# insert csv data to db
def insert_restaurant_data(restaurant_path):
    with open(restaurant_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Create a new restaurant instance for each row in the CSV
            score = float(row['Score']) if row['Score'] and row['Score'] != 'None' else None
            price_range = int(row['Price_range']) if row['Price_range'] and row['Price_range'] != 'None' else None
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


@app.route('/')
def log_in_page():
    return render_template('login.html')


@app.route('/log_in', methods=['POST'])
def loh_in():
    username = request.form['username']
    password = request.form['password']
    exist_username = User.query.filter_by(username=username).first()
    password_true = User.query.filter_by(username=username, password=password).first()
    if not exist_username:
        flash('Username doesn\'t exists.', 'error')
        return redirect(url_for('log_in_page'))
    elif not password_true:
        flash('Wrong Password', 'error')
        return redirect(url_for('log_in_page'))
    else:
        session['username'] = username
        return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    if not username:
        return redirect(url_for('log_in_page'))

    if request.method == 'POST':
        # Retrieve checkbox values from the form data
        zips = request.form.get('zipcode', '')
        if zips == '':
            zips = None
        zips = zips.strip()
        # Stars
        selected_star_range = request.form.get('star', '')
        if selected_star_range == '':
            selected_star_range = None

        # Price ranges
        selected_price_range = request.form.get('price_range', '')
        if selected_price_range == '':
            selected_price_range = None

        # Category
        selected_category = request.form.get('category', '')
        if selected_category == '':
            selected_category = None

        # SQL query
        string_query = "select * from Restaurant where 1=1"
        params = {}

        if zips is not None:
            string_query = string_query + " and (Restaurant.zip = :zip)"
            params["zip"] = zips
        if selected_star_range is not None:
            string_query = string_query + " and (Restaurant.score >= :star)"
            params["star"] = int(selected_star_range)
        if selected_price_range is not None:
            string_query = string_query + " and (Restaurant.price_range <= :price_range)"
            params["price_range"] = int(selected_price_range)
        if selected_category is not None:
            string_query = string_query + " and Restaurant.restaurant_id in (select r.restaurant_id from Restaurant r left join restaurant_category rc on r.restaurant_id=rc.restaurant_id where rc.Category_type = :category)"
            params["category"] = selected_category

        query = text(string_query)
        # params = {"zip": zips, "star": selected_star_range, 'price_range': selected_price_range, 'category':selected_category}
        # zip_query = text("INTERSECT select * from Restaurant where (Restaurant.zip = :zip)")
        # star_query = text("INTERSECT select * from Restaurant where Restaurant.score >= :star")
        # price_query = text("INTERSECT select * from Restaurant where Restaurant.price_range <= :price_range")
        # category_query = text("INTERSECT select * from Restaurant where Restaurant.restaurant_id in (select distinct Restaurant_id from restaurant_category where Category_type = :category)")

        # Execute the query
        result = db.session.execute(query, params)

        # Fetch the results
        restaurants = result.fetchall()
        #return render_template('DashBoard.html', user=user, username=username, restaurants=restaurants)
    else:
        restaurants = Restaurant.query.limit(1000).all()

    restaurant_keywords = request.args.get('keywords', '')
    if restaurant_keywords:
        restaurant_keywords = restaurant_keywords.strip()
        print(f"Selected keywords: {restaurant_keywords}")
        string_keyword = """
                             select distinct r.restaurant_id, r.restaurant_name, r.score, r.price_range, r.street, r.city, r.state, r.zip
                             from Restaurant r 
                             left join restaurant_category rc 
                             on r.restaurant_id=rc.restaurant_id 
                             where r.restaurant_name like :keyword
                                 or r.street like :keyword
                                 or r.city like :keyword
                                 or rc.Category_type like :keyword
                                  """
        params2 = {'keyword': f"%{restaurant_keywords}%"}
        key_word_query = text(string_keyword)
        result2 = db.session.execute(key_word_query, params2)

        # Fetch the results
        restaurants2 = result2.fetchall()
    else:
        restaurants2 = Restaurant.query.limit(1000).all()

    string_user_resturant = """
                            select distinct r.restaurant_id, r.restaurant_name, r.score, r.price_range, r.street, r.city, r.state, r.zip
                            from Favorite f
                            left join Restaurant r
                            on f.restaurant_id = r.restaurant_id
                            where f.user_id = :user_id
                            """
    params3 = {'user_id': user.user_id}
    favorite_restaurant_query = text(string_user_resturant)
    result3 = db.session.execute(favorite_restaurant_query, params3)
    # Fetch the results
    favorite_restaurant = result3.fetchall()

    return render_template('DashBoard.html', user=user, username=username, restaurants=restaurants,
                           restaurants2=restaurants2, favorite_resturant=favorite_restaurant)


@app.route('/register')
def register():
    users = User.query.all()
    return render_template('Register.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    user_exist = User.query.filter_by(username=username).first()
    if user_exist:
        flash('Username already exists. Please choose another one.', 'error')
        return redirect(url_for('register'))
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

    return redirect(url_for('register'))


@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('register'))


@app.route('/Add_Favorite/<int:restaurant_id>')
def add_favorite(restaurant_id):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    already_like = Favorite.query.filter_by(user_id=user.user_id, restaurant_id=restaurant_id).first()

    if not already_like:
        new_restaurant = Favorite(
            user_id=user.user_id,
            restaurant_id=restaurant_id
        )
        db.session.add(new_restaurant)
        db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/delete_favorite/<int:restaurant_id>')
def delete_favorite(restaurant_id):
    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    favorite_to_delete = Favorite.query.filter_by(user_id=user.user_id, restaurant_id=restaurant_id).first()
    db.session.delete(favorite_to_delete)
    db.session.commit()
    return redirect(url_for('dashboard'))


# Add a new route for the register page
@app.route('/redirect_to_register')
def redirect_to_register():
    return redirect(url_for('register'))


# Add a new route for the login page
@app.route('/redirect_to_login')
def redirect_to_login():
    return redirect(url_for('log_in_page'))


@app.route('/menu/<int:restaurant_id>')
def menu(restaurant_id):
    # restaurant_id = request.args.get('restaurant_id')
    print(restaurant_id)
    restaurant = Restaurant.query.get(restaurant_id)
    dishes = Dish.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, dishes=dishes)


# Add a new route for the login page
@app.route('/redirect_to_dashboard')
def redirect_to_dashboard():
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # csv paths
    restaurant_path = 'CSV_DATA/restaurant_dataset.csv'
    restaurant_menus_path = 'CSV_DATA/restaurant_menus.csv'
    categories_path = 'CSV_DATA/categories.csv'
    # test path
    restaurant_short_path = 'CSV_DATA/restaurant_short.csv'
    categories_short_path = 'CSV_DATA/categories_short.csv'
    restaurant_menus_short_path = 'CSV_DATA/restaurant_menus_short.csv'
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_restaurant_data(restaurant_short_path)
        insert_restaurant_category_data(categories_short_path)
        insert_dish_data(restaurant_menus_short_path)
    app.run(debug=True)
