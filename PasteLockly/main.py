from flask import Flask, request, redirect, render_template
from models import db, TextSnippet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snippets.db'
db.init_app(app)

@app.route('/')
def index():
    snippets = TextSnippet.query.all()
    return render_template('index.html', snippets=snippets)

@app.route('/add', methods=['POST'])
def add_snippet():
    text = request.form.get('text')
    if text:
        snippet = TextSnippet(text=text)
        db.session.add(snippet)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
