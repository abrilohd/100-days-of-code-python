# Day 17 Mini Project
# Bank Account System using Classes

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
            return
        self.balance -= amount
        print(f"Withdrew {amount}. New balance: {self.balance}")

    def show_account(self):
        print("\n--- Account Info ---")
        print(f"Owner: {self.owner}")
        print(f"Balance: {self.balance}")


# Program starts here
account = BankAccount("Abrham")

while True:
    print("\n1. Deposit")
    print("2. Withdraw")
    print("3. Show Account")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        amount = float(input("Enter amount to deposit: "))
        account.deposit(amount)

    elif choice == "2":
        amount = float(input("Enter amount to withdraw: "))
        account.withdraw(amount)

    elif choice == "3":
        account.show_account()

    elif choice == "4":
        print("Thank you for using the bank system.")
        break

    else:
        print("Invalid choice. Try again.")
