import logging

logging.basicConfig(level=logging.INFO)

class User:
    def __init__(self, name, age, gender) -> None:
        """ Initialize a new User object with name, age, and gender"""
        self._name = name 
        self._age = age
        self._gender = gender

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
        Display the details of the user
        """
        logging.info(f"Name: {self.name}")
        logging.info(f"Age: {self.age}")
        logging.info(f"Gender: {self.gender}")

class Bank(User):
    def __init__(self, name, age, gender ) -> None:
        super().__init__(name, age, gender)
        self._balance = 0

    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount):
        """
        Deposit the specified amount into the account and update the balance
        """
        if amount <=0:
            logging.info(f"Deposit amount should be greater than zero.")
            return
        self._balance += amount
        logging.info(f"Deposit successful. Account balance: $ {self.balance}")

    
    def withdraw(self, amount):
        """
        Withdraw the specified amount from the bank and update the balance
        """
        if amount <= 0:
            logging.error("Withdraw amount should be greater than zero")
            return
        if amount > self.balance:
            logging.error("Insufficient funds.")
            return
        self._balance -= amount
        logging.info(f"Withdraw successful. Account balance: $ {self.balance}")


    def view_balance(self):
        """
        Display the User details and the current account balance
        """

        self.view_detail()
        logging.info(f"Account balance: $ {self.balance}")

#Usage
 
bank_user = Bank("Edison", 20, "Male")
bank_user.view_detail()  # Display user details
bank_user.deposit(3000)  # Deposit an amount
bank_user.withdraw(2000)  # Withdraw an amount
bank_user.view_balance()  # Display user details and account balance
