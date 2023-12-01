import csv
from sqlalchemy import text
from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_init import db, Restaurant, restaurant_category, Dish, User, Favorite  

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
## start
db.init_app(app)

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

    # Initialize variables
    restaurants, restaurants2, favorite_restaurant = [], [], []
    active_tab = 'RestaurantList'  # Default active tab
    error_message = ''
    error_message2 = '' 

    if request.method == 'POST':
        # Retrieve and process form data
        zips = request.form.get('zipcode', '')
        selected_star_range = request.form.get('star', '')
        selected_price_range = request.form.get('price_range', '')
        selected_category = request.form.get('category', '')
        
        if not zips:
            error_message = 'Please enter a ZIP code.'
        else:

            # Create SQL query
            string_query = "select * from Restaurant where 1=1"
            params = {}
            if zips:
                string_query += " and Restaurant.zip = :zip"
                params["zip"] = zips
            if selected_star_range:
                string_query += " and Restaurant.score >= :star"
                params["star"] = selected_star_range
            if selected_price_range:
                string_query += " and Restaurant.price_range <= :price_range"
                params["price_range"] = selected_price_range
            if selected_category:
                # Corrected subquery
                string_query += " and Restaurant.restaurant_id in (select rc.restaurant_id from restaurant_category rc where rc.Category_type = :category)"
                params["category"] = selected_category

            # Execute query
            query = text(string_query)
            result = db.session.execute(query, params)
            restaurants = result.fetchall()
            if not restaurants:
                error_message = "No restaurants found matching your criteria."
        
    # Handling GET request (for keyword search)
    restaurant_keywords = request.args.get('keywords', '')
    if restaurant_keywords:
        active_tab = 'KeywordSearch'
        string_keyword = """
            select distinct r.restaurant_id, r.restaurant_name, r.score, r.price_range, r.street, r.city, r.state, r.zip
            from Restaurant r 
            left join restaurant_category rc on r.restaurant_id=rc.restaurant_id 
            where r.restaurant_name like :keyword
            or r.street like :keyword
            or r.city like :keyword
            or rc.Category_type like :keyword
            LIMIT 50
        """
        params2 = {'keyword': f"%{restaurant_keywords}%"}
        key_word_query = text(string_keyword)
        result2 = db.session.execute(key_word_query, params2)
        restaurants2 = result2.fetchall()
        if not restaurants2:
            error_message2 = "No restaurants found matching your keywords."
       

    # Handling Favorites
    string_user_resturant = """
        select distinct r.restaurant_id, r.restaurant_name, r.score, r.price_range, r.street, r.city, r.state, r.zip
        from Favorite f
        left join Restaurant r on f.restaurant_id = r.restaurant_id
        where f.user_id = :user_id
        LIMIT 50
    """
    params3 = {'user_id': user.user_id}
    favorite_restaurant_query = text(string_user_resturant)
    result3 = db.session.execute(favorite_restaurant_query, params3)
    favorite_restaurant = result3.fetchall()

    return render_template('DashBoard.html', user=user, username=username, 
                           restaurants=restaurants, restaurants2=restaurants2, 
                           favorite_resturant=favorite_restaurant, active_tab=active_tab,
                           error_message=error_message, error_message2=error_message2)



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
    with app.app_context():
        # This will ensure all tables are created
        db.create_all()
    app.run(debug=True)
