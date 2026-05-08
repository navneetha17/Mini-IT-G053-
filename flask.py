from flask import Flask, render_template, request, redirect 
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
 return "Home Page"

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
  
  if request.method == 'POST':
     
     username = request.form['username']
     password = request.form['password']

     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

     print(username)
     print(hashed_password)

     return redirect('/login')

  return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  
  if request.method == 'POST':
     
     username = request.form['username']
     password = request.form['password']

     stored_password = "$2b$12$examplehash"

     if bcrypt.check_password_hash(stored_password, password):

        return "Login Successful"
     
     else:
        return "Wrong Password"
  
  return render_template('login.html')