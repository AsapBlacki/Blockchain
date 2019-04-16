from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blocks.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class Blocks(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    hashPrecedent = db.Column(db.String(1000))
    data = db.Column(db.String(100))
    date = db.Column(db.String(50))
    random = db.Column(db.Integer)

    def __init__(self, p_hash_precedent, p_data, p_date, p_random):
        self.HashPrecedent = p_hash_precedent
        self.Data = p_data
        self.Date = p_date
        self.Random = p_random


@app.route('/')
def show_all():
    return render_template('show_all.html', blocks=Blocks.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['hash_precedent'] or not request.form['data'] or not request.form['date']\
                or not request.form['random']:
            flash('Svp veuillez saisir tous les champs', 'erreur')
        else:
            block = Blocks(request.form['hash_precedent'], request.form['data'],
                           request.form['date'], request.form['random'])

            db.session.add(block)
            db.session.commit()
            flash('Les enregistrements ont été correctement ajoutés')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
