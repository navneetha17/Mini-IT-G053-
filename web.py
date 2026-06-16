from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route('/')
def home():
    return redirect(url_for('login'))

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Missing username or password"

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return redirect(url_for('home_page'))
        else:
            return "Wrong Username or Password"

    return render_template('login.html')

# REGISTER 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password:
            return "Missing fields"

        if password != confirm_password:
            return "Passwords do not match"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# HOME PAGE 
@app.route('/home')
def home_page():
    return render_template('main_page.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    # If someone opens URL manually → redirect safely
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