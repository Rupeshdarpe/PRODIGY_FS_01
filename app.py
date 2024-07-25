from flask import Flask , request, render_template, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL  # db connection
from flask_bcrypt import Bcrypt #for encryption of passw

app = Flask(__name__)
app.secret_key = '49495abdklfjbdklflaskfd'

#MySQL configuration
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "flask_db"

mysql = MySQL(app)
login_manage = LoginManager()
login_manage.init_app(app)
bcrypt = Bcrypt(app)

#User Loader function
@login_manage.user_loader
def load_user(user_id):
    return User.get(user_id)

class User(UserMixin):
    def __init__(self, user_id,name, email,):
        self.id = user_id
        self.name = name
        self.email = email
      

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT name,email from users where id = %s',(user_id))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(user_id, result[0], result[1])


@app.route('/')
def index():
    return 'Home page'

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor() 
        cursor.execute('SELECT id, name, email, password FROM users WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect(url_for('dashboard'))

        # If login fails, return a response to indicate the failure (e.g., render login.html with an error message)
        return render_template("login.html")  # Render login page with error message (optional)

    # For GET requests (initial rendering of login page)
    return render_template("login.html")


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
       name = request.form['name']
       email = request.form['email']
       password = request.form['password']

       hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') #to encryp password
       
       cursor = mysql.connection.cursor() 

       cursor.execute('INSERT INTO users (name, email, password) values(%s, %s, %s)',(name, email, hashed_password))
       mysql.connection.commit()
       cursor.close()
       return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__=='__main__':
    app.run(debug=True)

# from flask import Flask, request, render_template, redirect, url_for
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from flask_mysqldb import MySQL #DB connection
# from flask_bcrypt import Bcrypt # encryption

# app = Flask(__name__)
# app.secret_key = '49495abdklfjbdklflaskfd'

# # MySQL configuration
# app.config['MYSQL_HOST'] = "localhost"
# app.config['MYSQL_USER'] = "root"
# app.config['MYSQL_PASSWORD'] = "root"
# app.config['MYSQL_DB'] = "flask_db"

# mysql = MySQL(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# bcrypt = Bcrypt(app)

# # User Loader function
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

# class User(UserMixin):
#     def __init__(self, user_id, name, email):
#         self.id = user_id
#         self.name = name
#         self.email = email

#     @staticmethod
#     def get(user_id):
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT name, email FROM users WHERE id = %s', (user_id,))
#         result = cursor.fetchone()
#         cursor.close()
#         if result:
#             return User(user_id, result[0], result[1])
#         return None  # Handle case where user_id is not found

# @app.route('/')
# def index():
#     return 'Home page'

# @app.route('/login', methods=['POST','GET'])
# def login():
#     if request.method == "POST":
      
#        email = request.form['email']
#        password = request.form['password']
      
#        cursor = mysql.connection.cursor() 

#        cursor.execute('SELECT id, name, email, password from users where email = %s', (email,))
#        user_data = cursor.fetchone()  
#        cursor.close()
       
#        if user_data and bcrypt.check_password_hash(user_data[3], password): # 3 because password is at 3rd place
#         user = User(user_data[0], user_data[1], user_data[2])
#         login_user(user)
#         return redirect(url_for('dashboard'))
       
#         return render_template("login.html")

# @app.route('/register', methods=['POST','GET'])
# def register():
#     if request.method == "POST":
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']

#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

#         cursor = mysql.connection.cursor()
#         cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
#         mysql.connection.commit()
#         cursor.close()

#         return redirect(url_for('login'))

#     return render_template("register.html")

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return 'Dashboard Page'

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
