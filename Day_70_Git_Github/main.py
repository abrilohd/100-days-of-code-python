from flask import Flask
from getname import random_name
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_KEY", "dev-key")


@app.route("/")
def hello_world():
    return f"<h1>Behold, I am {random_name('superhero')}!</h1>"


if __name__ == "__main__":
    app.run(debug=True)