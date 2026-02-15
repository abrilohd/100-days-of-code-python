from flask import Flask
import time 

app = Flask(__name__)

def bold(function):
    def wrrapper_function():
        return f"<b>{function()}</b>"
    return wrrapper_function

def under_line(function):
    def wrraper():
        return f"<u>{function()}</u>"
    return wrraper

def make_enphasis(function):
    def wrraper():
        return f"<em>{function()}</em>"
    return wrraper


@app.route("/bye")
@bold
@under_line
@make_enphasis
def bye():
    return "Bye see you"

@app.route('/')
def hello_world():
    return '<h1 style="text-align: center;">Hello, World!</h1>\
        <p>This is the paragraph</p>\
        <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXp3cDkxa3E4MDB1b2lsaDRydHF2bHRqZ3N2amdxcWNjaGVieXlzeSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Q1JFTKT3sEWiGkvPDq/giphy.gif">'

@app.route("/<text>/<int:num>")
def say_bye(text, num):
    return f"Bye you and {text} and your {num}"

## ********Day 55 Start**********

## Advanced Python Decorator Functions

class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])
    return wrapper

@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")

new_user = User("angela")
new_user.is_logged_in = True
create_blog_post(new_user)

if __name__ == "__main__":
    app.run(debug=True)

