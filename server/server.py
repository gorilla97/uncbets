from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create app instance
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uncbets_user:your_password@localhost/uncbets_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Add other user login information fields

class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    acceptor_id = db.Column(db.Integer)
    bet_worth = db.Column(db.Float)
    bet_body = db.Column(db.String(255))
    bet_status = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# Route to handle user registration
@app.route("/api/register", methods=['POST'])
def register_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

# Route to handle user login
@app.route("/api/login", methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# Route to get all bets
@app.route("/api/bets", methods=['GET'])
def get_all_bets():
    bets = Bet.query.all()
    bet_list = []
    for bet in bets:
        bet_list.append({
            'id': bet.id,
            'creator_id': bet.creator_id,
            'acceptor_id': bet.acceptor_id,
            'bet_worth': bet.bet_worth,
            'bet_body': bet.bet_body,
            'bet_status': bet.bet_status
        })
    return jsonify({"bets": bet_list})

# Route to create a new bet
@app.route("/api/bets", methods=['POST'])
def create_bet():
    data = request.json
    new_bet = Bet(
        creator_id=data['creator_id'],
        acceptor_id=data['acceptor_id'],
        bet_worth=data['bet_worth'],
        bet_body=data['bet_body'],
        bet_status=data['bet_status']
    )
    db.session.add(new_bet)
    db.session.commit()
    return jsonify({"message": "Bet created successfully"})

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8000)