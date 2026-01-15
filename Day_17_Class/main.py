# Day 17 - Level Up Python Classes

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_logged_in = False

    def login(self):
        self.is_logged_in = True
        print(f"{self.username} logged in.")

    def logout(self):
        self.is_logged_in = False
        print(f"{self.username} logged out.")

    def show_profile(self):
        print("\n--- User Profile ---")
        print(f"Username: {self.username}")
        print(f"Email: {self.email}")
        print(f"Logged In: {self.is_logged_in}")


# Creating objects
user1 = User("abel", "abel@email.com")
user2 = User("sara", "sara@email.com")

user1.login()
user1.show_profile()

user2.show_profile()
