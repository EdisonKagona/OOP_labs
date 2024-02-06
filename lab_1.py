class User:
    def __init__(self, name, age, gender):
        """
        Initialize a new User object with name, age, and gender.
        """
        self.name = name 
        self.age = age
        self.gender = gender 

    def view_detail(self):
        """
        Display the details of the user.
        """
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")

class Bank(User):
    def __init__(self, name, age, gender):
        """
        Initialize a new Bank object with name, age, gender, and a balance of 0.
        """
        super().__init__(name, age, gender)
        self.balance = 0

    def deposit(self, amount):
        """
        Deposit the specified amount into the account and update the balance.
        """
        self.amount = amount 
        self.balance += amount
        print(f"Account balance has been updated: $ {self.balance}")

    def withdraw(self, amount):
        """
        Withdraw the specified amount from the account and update the balance.
        """
        self.amount = amount
        if amount > self.balance:
            print(f"Insufficient Funds | Balance available: $ {self.balance}")
        else:
            self.balance -= amount
            print(f"Account balance has been updated: $ {self.balance}")

    def view_balance(self):
        """
        Display the user details and the current account balance.
        """
        self.view_detail()
        print(f"Account balance: $ {self.balance}")


# Usage 
bank_user = Bank("Edison", 20, "Male")
bank_user.view_detail()  # Display user details
bank_user.deposit(3000)  # Deposit an amount
bank_user.withdraw(2000)  # Withdraw an amount
bank_user.view_balance()  # Display user details and account balance
