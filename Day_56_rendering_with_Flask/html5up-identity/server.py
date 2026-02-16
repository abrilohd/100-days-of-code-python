from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

@app.route('/hello')
def hello(name = None):
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)