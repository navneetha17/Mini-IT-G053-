from flask import Flask, render_template, request, redirect, session, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.secret_key = "your_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_name = db.Column(db.String(200), nullable=False)


# HOME ROUTE
@app.route('/')
def home():
    return redirect(url_for('login'))


# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home_page'))

        return "Wrong Username or Password"

    return render_template('login.html')


# REGISTER ROUTE
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return "Passwords do not match"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


# RESTAURANT PAGE ROUTE
@app.route('/restaurant/<path:restaurant_name>')
def restaurant(restaurant_name):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    with open('data/restaurants.json', 'r') as f:
        data = json.load(f)

    restaurant_data = None

    for r in data:
        if r['name'] == restaurant_name:
            restaurant_data = r
            break

    if not restaurant_data:
        return "Restaurant not found"

    fav_list = Favourite.query.filter_by(
        user_id=session['user_id']
    ).all()

    fav_names = [f.restaurant_name for f in fav_list]

    return render_template(
        'results.html',
        results=[restaurant_data],
        fav_names=fav_names
    )


# ADD FAVOURITE ROUTE
@app.route('/favourite', methods=['POST'])
def favourite():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    restaurant_name = request.form['restaurant_name']

    fav = Favourite(
        user_id=session['user_id'],
        restaurant_name=restaurant_name
    )

    db.session.add(fav)
    db.session.commit()

    return redirect(request.referrer or url_for('favourites'))


# DELETE FAVOURITE ROUTE
@app.route('/delete_favourite/<restaurant_name>')
def delete_favourite(restaurant_name):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    fav = Favourite.query.filter_by(
        user_id=session['user_id'],
        restaurant_name=restaurant_name
    ).first()

    if fav:
        db.session.delete(fav)
        db.session.commit()

    return redirect(request.referrer or url_for('favourites'))


# VIEW FAVOURITES ROUTE
@app.route('/favourites')
def favourites():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    favourites = Favourite.query.filter_by(
        user_id=session['user_id']
    ).all()

    return render_template('favourites.html', favourites=favourites)


# HOME PAGE ROUTE
@app.route('/home')
def home_page():
    return render_template('main_page.html')


# RECOMMEND ROUTE
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():

    if request.method == 'GET':
        return redirect(url_for('home_page'))

    category = request.form.get('category')
    budget = request.form.get('budget')

    with open('data/restaurants.json', 'r') as f:
        data = json.load(f)

    results = []

    for item in data:
        if item['category'] != category:
            continue

        price = item['price']

        if budget == "5-9" and 5 <= price <= 9:
            results.append(item)
        elif budget == "10-15" and 10 <= price <= 15:
            results.append(item)
        elif budget == "16-20" and 16 <= price <= 20:
            results.append(item)
        elif budget == "21-31" and 21 <= price <= 31:
            results.append(item)

    return render_template('results.html', results=results)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

    