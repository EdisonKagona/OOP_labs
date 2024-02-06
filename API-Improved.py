from flask import Flask, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import sys
import gettext  # For internationalization support

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure internationalization
gettext.install('messages', localedir=None, unicode=True)

app = Flask(__name__)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "200 per hour"]
)

class User:
    def __init__(self, name, password, age, gender):
        """
        Initialize a new User object with name, age, gender, and password.
        """
        self._name = name 
        self._password = generate_password_hash(password)
        self._age = self._validate_age(age)
        self._gender = self._validate_gender(gender)

    @property
    def name(self):
        return self._name
    
    @property
    def password(self):
        return self._password
    
    @property
    def age(self):
        return self._age
    
    @property
    def gender(self):
        return self._gender
    
    def view_detail(self):
        """
        Display the details of the user.
        """
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

    def _validate_age(self, age):
        """
        Validate the age input.
        """
        if not isinstance(age, int) or age <= 0:
            logging.error(_("Invalid age. Age should be a positive integer."))
            raise ValueError(_("Invalid age. Age should be a positive integer."))
        return age

    def _validate_gender(self, gender):
        """
        Validate the gender input.
        """
        allowed_genders = ["Male", "Female", "Other"]
        if gender not in allowed_genders:
            logging.error(_("Invalid gender. Gender should be 'Male', 'Female', or 'Other'."))
            raise ValueError(_("Invalid gender. Gender should be 'Male', 'Female', or 'Other'."))


class Bank:
    def __init__(self, user):
        """
        Initialize a new Bank object with a User instance and a balance of 0.
        """
        self._user = user
        self._balance = 0

    @property
    def user(self):
        return self._user

    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount):
        """
        Deposit the specified amount into the account and update the balance.
        """
        if not isinstance(amount, (int, float)):
            logging.error(_("Invalid amount. Please provide a valid number."))
            return
        if amount <= 0:
            logging.error(_("Deposit amount should be greater than zero."))
            return
        self._balance += amount
        logging.info(_("Deposit successful. Account balance: $ {self.balance}"))

    
    def withdraw(self, amount):
        """
        Withdraw the specified amount from the account and update the balance.
        """
        if not isinstance(amount, (int, float)):
            logging.error(_("Invalid amount. Please provide a valid number."))
            return
        if amount <= 0:
            logging.error(_("Withdrawal amount should be greater than zero."))
            return
        if amount > self.balance:
            logging.error(_("Insufficient funds."))
            return
        self._balance -= amount
        logging.info(_("Withdrawal successful. Account balance: $ {self.balance}"))

    def view_balance(self):
        """
        Display the user details and the current account balance.
        """
        return {
            "user_details": self.user.view_detail(),
            "account_balance": self.balance
        }


class AuthManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AuthManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._users = {}
        return cls._instance

    def register_user(self, user):
        """
        Register a new user in the system.
        """
        self._users[user.name] = user

    def authenticate(self, name, password):
        """
        Authenticate a user based on their name and password.
        """
        user = self._users.get(name)
        if user and check_password_hash(user.password, password):
            return user
        return None


# Routes
auth_manager = AuthManager()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not all(key in data for key in ['name', 'password', 'age', 'gender']):
        return jsonify({'error': 'Missing required parameters'}), 400
    try:
        user = User(data['name'], data['password'], data['age'], data['gender'])
        auth_manager.register_user(user)
        return jsonify({'message': 'User registered successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    if not all(key in data for key in ['name', 'password']):
        return jsonify({'error': 'Missing required parameters'}), 400
    user = auth_manager.authenticate(data['name'], data['password'])
    if user:
        access_token = create_access_token(identity=user.name)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/bank/deposit', methods=['POST'])
@jwt_required()
@limiter.limit("1000 per day")
def deposit():
    data = request.json
    if not all(key in data for key in ['amount']):
        return jsonify({'error': 'Missing required parameters'}), 400
    current_user = get_jwt_identity()
    user = auth_manager._users.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        amount = float(data['amount'])
        bank = Bank(user)
        bank.deposit(amount)
        return jsonify({'message': 'Deposit successful'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/bank/withdraw', methods=['POST'])
@jwt_required()
@limiter.limit("1000 per day")
def withdraw():
    data = request.json
    if not all(key in data for key in ['amount']):
        return jsonify({'error': 'Missing required parameters'}), 400
    current_user = get_jwt_identity()
    user = auth_manager._users.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    try:
        amount = float(data['amount'])
        bank = Bank(user)
        bank.withdraw(amount)
        return jsonify({'message': 'Withdrawal successful'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/bank/balance', methods=['GET'])
@jwt_required()
def get_balance():
    current_user = get_jwt_identity()
    user = auth_manager._users.get(current_user)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    bank = Bank(user)
    return jsonify(bank.view_balance()), 200

if __name__ == "__main__":
    app.run(debug=True)
