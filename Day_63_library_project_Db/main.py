from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
import os
from dotenv import load_dotenv

# ---------------------- CONFIG ---------------------- #
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "books.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Bootstrap5(app)

# ---------------------- DATABASE ---------------------- #
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


with app.app_context():
    db.create_all()

# ---------------------- FORMS ---------------------- #
class BookForm(FlaskForm):
    title = StringField("Book Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    rating = FloatField(
        "Rating (0-10)",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=10, message="Rating must be between 0 and 10.")
        ],
    )
    submit = SubmitField("Add Book")


class EditForm(FlaskForm):
    rating = FloatField(
        "New Rating (0-10)",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=10)
        ],
    )
    submit = SubmitField("Update Rating")


# ---------------------- ROUTES ---------------------- #
@app.route("/")
def home():
    books = db.session.execute(db.select(Book).order_by(Book.rating.desc())).scalars().all()
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()

    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            rating=form.rating.data,
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add.html", form=form)


@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    book = db.get_or_404(Book, book_id)
    form = EditForm()

    if form.validate_on_submit():
        book.rating = form.rating.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", book=book, form=form)


@app.route("/delete/<int:book_id>")
def delete(book_id):
    book = db.get_or_404(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
