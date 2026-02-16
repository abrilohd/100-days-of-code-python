from flask import Flask, render_template, abort
import requests

app = Flask(__name__)

# Replace this with your own npoint.io endpoint if you created one.
# Example: https://api.npoint.io/<your-id>
NPOINT_URL = "https://api.npoint.io/531caaf196da9241d4c9"


@app.route("/")
def home():
    try:
        response = requests.get(NPOINT_URL, timeout=5)
        response.raise_for_status()
        posts = response.json()
    except Exception:
        posts = []

    # Pass blog header strings plus posts to the template
    return render_template(
        "index.html",
        posts=posts,
        blog_title="Clean Blog",
        blog_subtitle="A Blog Theme by Start Bootstrap",
    )


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/post/<int:post_id>')
def show_post(post_id):
    try:
        response = requests.get(NPOINT_URL, timeout=5)
        response.raise_for_status()
        posts = response.json()
    except Exception:
        posts = []

    # Guard against out-of-range IDs
    if not posts or post_id < 0 or post_id >= len(posts):
        return render_template('post.html', post=None)

    post = posts[post_id]
    return render_template('post.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)