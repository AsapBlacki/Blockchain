from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blocks.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class Blocks(db.Model):
    id = db.Column('block_id', db.Integer, primary_key=True)
    hash_precedent = db.Column(db.String(1000))
    data = db.Column(db.String(100))
    date = db.Column(db.String(50))
    random = db.Column(db.Integer)

    def __init__(self, p_hash_precedent, p_data, p_date, p_random):
        self.hash_precedent = p_hash_precedent
        self.data = p_data
        self.date = p_date
        self.random = p_random


class Transaction(db.Model):
    id = db.Column('transacion_id', db.Integer, primary_key=True)
    adresse_expediteur = db.Column(db.String(2048))
    adresse_receveur = db.Column(db.String(2048))
    nombre_envoie = db.Column(db.Integer)
    etat = db.Column(db.Integer)

    def __init__(self, p_adresse_expediteur, p_adresse_receveur, p_nombre_envoie, p_etat):
        self.adresse_expediteur = p_adresse_expediteur
        self.adresse_receveur = p_adresse_receveur
        self.nombre_envoie = p_nombre_envoie
        self.etat = p_etat


class Portefeuilles(db.Model):
    id = db.Column('portefeuille_id', db.Integer, primary_key=True)
    private_key = db.Column(db.String(2048))
    public_key = db.Column(db.String(2048))
    balance = db.Column(db.Integer)

    def __init__(self, p_private_key, p_public_key, p_balance):
        self.private_key = p_private_key
        self.public_key = p_public_key
        self.balance = p_balance


@app.route('/')
def show_all():
    return render_template('show_all.html', blocks=Blocks.query.all())


@app.route('/portefeuille')
def portefeuille():
    return render_template('portefeuille.html', portefeuilles=Portefeuilles.query.all())


@app.route('/new.html', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['hash_precedent'] or not request.form['data'] or not request.form['date']\
                or not request.form['random']:
            flash('Svp veuillez saisir tous les champs', 'erreur')
        else:
            block = Blocks(request.form['hash_precedent'], request.form['data'],
                           request.form['date'], request.form['random'])

            transaction = Transaction(request.form['adresse_expediteur'], request.form['adresse_receveur'],
                                      request.form['nombre_envoie'], request.form['etat'])

            portefeuille = Portefeuille(request.form['private_key'], request.form['public_key'],
                                        request.form['balance'])

            db.session.add(block)
            db.session.add(transaction)
            db.session.add(portefeuille)
            db.session.commit()
            flash('Les enregistrements ont été correctement ajoutés')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
