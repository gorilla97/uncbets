from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_principal import Principal, Permission, RoleNeed

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'supersecretkey!'

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
principal = Principal(app)

# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'uncbets_user',
    'password': 'your_password',
    'database': 'uncbets_db',
}

# Define the User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

# Function to create a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Permission for admin role (if needed)
admin_permission = Permission(RoleNeed('admin'))

# Route for user registration
@app.route("/api/register", methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the username is already taken
        query = "SELECT * FROM user_table WHERE username = %s"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'Username is already taken'})

        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method='sha256')

        # Insert the user into the database
        query = "INSERT INTO user_table (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'User registered successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

# Route for user login
@app.route("/api/login", methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve the user from the database
        query = "SELECT * FROM user_table WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):  # Assuming password is stored in the third column
            # Use Flask-Login to log in the user
            user_obj = User(user[0], user[1])
            login_user(user_obj)
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid credentials'})

    except Exception as e:
        return jsonify({'error': str(e)})

# Flask-Login callback to load a user from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Retrieve the user from the database using user ID
    query = "SELECT * FROM user_table WHERE id = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        return User(user_data[0], user_data[1])
    else:
        return None

# Route for user logout
@app.route("/api/logout", methods=['POST'])
@login_required
def logout_user():
    logout_user()
    return jsonify({'message': 'Logout successful'})

# Update your existing "home" route to fetch and display bets
@app.route("/api/home", methods=['GET'])
@login_required
def return_home():
    user_id = current_user.id

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM bet_table WHERE creator_id = %s OR acceptor_id = %s"
        cursor.execute(query, (user_id, user_id))
        bets = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({'bets': bets})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=8000)