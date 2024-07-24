from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random
import validators

app = Flask(__name__)

# Config for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

# URL model
class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(6), unique=True, nullable=False)
    original_url = db.Column(db.String, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Function to generate a random short URL
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choice(characters) for _ in range(length))
        if not URLMapping.query.filter_by(short_url=short_url).first():
            break
    return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        if not validators.url(original_url):
            return 'Invalid URL', 400
        short_url = generate_short_url()
        new_url = URLMapping(short_url=short_url, original_url=original_url)
        db.session.add(new_url)
        db.session.commit()
        return f'Short URL is: {request.url_root}{short_url}'
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_url(short_url):
    url_entry = URLMapping.query.filter_by(short_url=short_url).first()
    if url_entry:
        return redirect(url_entry.original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
