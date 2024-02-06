import logging
import sys
import gettext  # For internationalization support

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure internationalization
gettext.install('messages', localedir=None, unicode=True)

class User:
    def __init__(self, name, age, gender):
        """
        Initialize a new User object with name, age, and gender.
        """
        self._name = name 
        self._age = self._validate_age(age)
        self._gender = self._validate_gender(gender)

    @property
    def name(self):
        return self._name
    
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
        logging.info(f"Name: {self.name}")
        logging.info(f"Age: {self.age}")
        logging.info(f"Gender: {self.gender}")

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
        return gender


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
        self.user.view_detail()
        logging.info(_("Account balance: $ {self.balance}"))


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

    def authenticate(self, name):
        """
        Authenticate a user based on their name.
        """
        return name in self._users


# Unit Testing
import unittest

class TestBank(unittest.TestCase):
    def setUp(self):
        self.user = User("Edison", 20, "Male")
        self.bank_user = Bank(self.user)

    def test_deposit(self):
        self.bank_user.deposit(3000)
        self.assertEqual(self.bank_user.balance, 3000)

    def test_withdraw(self):
        self.bank_user.deposit(3000)
        self.bank_user.withdraw(2000)
        self.assertEqual(self.bank_user.balance, 1000)

    def test_invalid_deposit(self):
        self.bank_user.deposit(-100)
        self.assertEqual(self.bank_user.balance, 0)

    def test_invalid_withdrawal(self):
        self.bank_user.deposit(1000)
        self.bank_user.withdraw(2000)
        self.assertEqual(self.bank_user.balance, 1000)

    def test_invalid_age(self):
        with self.assertRaises(ValueError):
            User("John", -30, "Male")

    def test_invalid_gender(self):
        with self.assertRaises(ValueError):
            User("Jane", 25, "Unknown")


if __name__ == "__main__":
    # Run unit tests
    unittest.main()

    # Usage 
    # auth_manager = AuthManager()
    # auth_manager.register_user(user)
    # auth_manager.authenticate("Edison")  # Returns True
    # bank_user.view_detail()  # Display user details
    # bank_user.deposit(3000)  # Deposit an amount
    # bank_user.withdraw(2000)  # Withdraw an amount
    # bank_user.view_balance()  # Display user details and account balance
