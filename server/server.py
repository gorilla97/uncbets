from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'supersecretkey!'

# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'uncbets_user',
    'password': 'your_password',
    'database': 'uncbets_db',
}

# Function to create a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

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
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid credentials'})

    except Exception as e:
        return jsonify({'error': str(e)})

def authenticate(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Retrieve the user from the database
    query = "SELECT * FROM user_table WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and safe_str_cmp(user[2], password):  # Assuming password is stored in the third column
        return user

def identity(payload):
    user_id = payload['identity']
    connection = get_db_connection()
    cursor = connection.cursor()

    # Retrieve the user from the database
    query = "SELECT * FROM user_table WHERE id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

jwt = JWT(app, authenticate, identity)

# Route for creating a new bet
@app.route("/api/create_bet", methods=['POST'])
def create_bet():
    data = request.get_json()
    creator_id = data.get('creator_id')
    acceptor_id = data.get('acceptor_id')
    bet_worth = data.get('bet_worth')
    bet_body = data.get('bet_body')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if acceptor_id is not None:
            # Update an existing bet (accept a bet)
            query = "UPDATE bet_table SET acceptor_id = %s, bet_status = 'accepted' WHERE id = %s"
            cursor.execute(query, (acceptor_id, creator_id))
        else:
            # Create a new bet
            query = "INSERT INTO bet_table (creator_id, bet_worth, bet_body, bet_status) VALUES (%s, %s, %s, 'pending')"
            cursor.execute(query, (creator_id, bet_worth, bet_body))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Bet processed successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})

# Update your existing "home" route to fetch and display bets
@app.route("/api/home", methods=['GET'])
def return_home(user_id):
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