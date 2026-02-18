from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv


load_dotenv() # This reads the .env file

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_SEARCH_URL = os.getenv("TMDB_SEARCH_URL")
TMDB_INFO_URL = os.getenv("TMDB_INFO_URL")
TMDB_IMAGE_URL = os.getenv("TMDB_IMAGE_URL")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, )
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(250))
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

## this runs once used to create the table 
# with app.app_context():
#     db.create_all()
#     # Check if the table is empty before adding the starter movie
#     if not db.session.execute(db.select(Movie)).first():
#         first_movie = Movie(
#             title="Phone Booth",
#             year=2002,
#             description="Publicist Stuart Shepard finds himself trapped...",
#             rating=7.3,
#             ranking=10,
#             review="My favourite character was the caller.",
#             img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#         )
#         db.session.add(first_movie)
#         db.session.commit()


def add_movie_if_not_exists(movie_data):
    # Check if a movie with this title is already in the DB
    existing_movie = db.session.execute(
        db.select(Movie).where(Movie.title == movie_data.title)
    ).scalar()

    if not existing_movie:
        db.session.add(movie_data)
        db.session.commit()
        print(f"Added: {movie_data.title}")
    else:
        print(f"Skipped: {movie_data.title} (Already exists)")

with app.app_context():
    db.create_all()
    
    # Define your movie
    new_movie = Movie(
        title="Avatar The Way of Water",
        year=2022,
        description="Set more than a decade after...",
        rating=7.3,
        ranking=9,
        review="I liked the water.",
        img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
    )

    # Use the helper function
    add_movie_if_not_exists(new_movie)


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")

# New Find Movie Form
class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    # 1. Get all movies ordered by rating (highest first)
    result = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())
    )

    movies = result.scalars().all()  # ← turn into a Python list

    # 2. Assign ranking based on order
    for index, movie in enumerate(movies):
        movie.ranking = index + 1

    db.session.commit()

    return render_template("index.html", movies=movies)


# Adding the Update functionality
@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete")
def delete():
    movie_id = request.args.get("id")

    movie = db.session.execute(
        db.select(Movie).where(Movie.id == movie_id)
    ).scalar()

    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(TMDB_SEARCH_URL, params={"api_key": TMDB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)
      
    return render_template("add.html", form=form)

@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        # 1. Use the /movie/ID endpoint, NOT the /search/movie endpoint
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        
        response = requests.get(movie_api_url, params={"api_key": TMDB_API_KEY, "language": "en-US"})
        data = response.json()
        poster_path = data.get("poster_path")
        poster_url = (
            f"https://image.tmdb.org/t/p/w500{poster_path}"
            if poster_path
            else "https://via.placeholder.com/300x450?text=No+Poster"
            )
        # Debugging: Print data if 'title' is missing to see the error from TMDB
        if "title" not in data:
            print(f"API Error: {data}")
            return "Movie details not found.", 404

        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0] if data.get("release_date") else "N/A",
            img_url=poster_url,
            description=data["overview"],
            rating=0.0,  # Provide a default float
            ranking=10,  # Provide a default int
            review="No review yet." # Provide a default string
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))



if __name__ == '__main__':
    app.run(debug=True)
