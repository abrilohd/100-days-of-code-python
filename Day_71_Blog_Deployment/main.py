# Standard library imports
import os
import smtplib
import hashlib
from functools import wraps
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy imports
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Security
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import Markup

# Forms
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Mail credentials
MAIL_ADDRESS = os.environ.get("MY_EMAIL")
MAIL_APP_PW = os.environ.get("MY_PASSWORD")

# Flask app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

database_url = os.environ.get("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
       
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize extensions
ckeditor = CKEditor(app)
Bootstrap5(app)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# SQLAlchemy Base and database initialization
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# For adding profile images to the comment section: local gravatar helper
def gravatar_url(email, size=100, default='retro', rating='g', use_ssl=False):
    email = (email or "").strip().lower()
    digest = hashlib.md5(email.encode('utf-8')).hexdigest()
    scheme = 'https' if use_ssl else 'http'
    return f"{scheme}://www.gravatar.com/avatar/{digest}?s={size}&d={default}&r={rating}"


@app.context_processor
def utility_processor():
    return dict(gravatar=gravatar_url)


# Also register as a Jinja filter so templates using the pipe syntax work:
@app.template_filter('gravatar')
def gravatar_filter(email, size=100, default='retro', rating='g', use_ssl=False):
    return gravatar_url(email, size=size, default=default, rating=rating, use_ssl=use_ssl)


# Provide a simple `render_form` global for templates if Bootstrap's helper isn't available.
@app.template_global()
def render_form(form, novalidate=False, button_map=None):
    try:
        # If Bootstrap-Flask provides a helper, prefer that
        from flask_bootstrap import render_form as _bf_render_form

        return _bf_render_form(form, novalidate=novalidate, button_map=button_map)
    except Exception:
        # Fallback: construct a basic form HTML
        attrs = ' novalidate' if novalidate else ''
        parts = [f"<form method=\"POST\"{attrs}>", form.hidden_tag()]
        for field in form:
            t = getattr(field, 'type', '')
            if t in ('CSRFTokenField', 'HiddenField'):
                continue
            if t == 'SubmitField':
                submit_field = field
                continue
            parts.append('<div class="mb-3">')
            parts.append(f'<label class="form-label">{field.label.text}</label>')
            parts.append(str(field(class_='form-control')))
            parts.append('</div>')
        # submit button
        try:
            submit_label = submit_field.label.text
        except Exception:
            submit_label = 'Submit'
        btn_class = 'btn btn-primary'
        if button_map and 'submit' in (button_map or {}):
            btn_class = f"btn btn-{button_map['submit']}"
        parts.append(f'<button type="submit" class="{btn_class}">{submit_label}</button>')
        parts.append('</form>')
        return Markup('\n'.join(parts))


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # Create reference to the User object. The "posts" refers to the posts property in the User class.
    author = relationship("User", back_populates="posts")
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # Parent relationship to the comments
    comments = relationship("Comment", back_populates="parent_post")


# Create a User table for all your registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    # This will act like a list of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")
    # Parent relationship: "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")


# Create a table for the comments on the blog posts
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    # Child relationship:"users.id" The users refers to the tablename of the User class.
    # "comments" refers to the comments property in the User class.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # Child Relationship to the BlogPosts
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")


with app.app_context():
    db.create_all()

# Admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is not logged in, redirect to login page
        if not current_user.is_authenticated:
            return redirect(url_for("login"))

        # If user is logged in but not admin (id != 1), show 403
        if current_user.id != 1:
            return abort(403)

        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, current_user=current_user)


# Register new users into the User database
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)

    # Find newer and older posts
    newer_post = BlogPost.query.filter(BlogPost.id > post_id).order_by(BlogPost.id.asc()).first()
    older_post = BlogPost.query.filter(BlogPost.id < post_id).order_by(BlogPost.id.desc()).first()

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))

    return render_template(
        "post.html",
        post=requested_post,
        current_user=current_user,
        form=comment_form,
        newer_post=newer_post,
        older_post=older_post
    )


# Use a decorator so only an admin user can create new posts
@app.route("/new-post", methods=["GET", "POST"])
# @login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, current_user=current_user)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only  # add this
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(
            data["name"],
            data["email"],
            data["phone"],
            data["message"]
        )
        return render_template("contact.html", msg_sent=True)

    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"""Subject: New Contact Message

Name: {name}
Email: {email}
Phone: {phone}
Message:
{message}
"""

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(
            os.environ.get("MY_EMAIL"),
            os.environ.get("MY_PASSWORD")
        )
        connection.sendmail(
            os.environ.get("MY_EMAIL"),
            os.environ.get("MY_EMAIL"),
            email_message
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)