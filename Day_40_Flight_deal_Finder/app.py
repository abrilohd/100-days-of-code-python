# app.py
from flask import Flask, render_template
from data_manager import DataManager

app = Flask(__name__)

@app.route("/")
def index():
    dm = DataManager()
    try:
        flights = dm.get_destination_data()
    except Exception as e:
        flights = []
        print("[app] Error fetching sheet data:", e)
    return render_template("index.html", flights=flights)

if __name__ == "__main__":
    app.run(debug=True)
