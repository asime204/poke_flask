from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, firstName, lastName, username, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    def saveChanges(self):
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    HP = db.Column(db.Integer, nullable=False)
    ATK = db.Column(db.Integer, nullable=False)
    DEF = db.Column(db.Integer, nullable=False)
    SPD = db.Column(db.Integer, nullable=False)
    Ability = db.Column(db.String(255), nullable=False)
    ImgURL = db.Column(db.String(255), nullable=True)
    user_pokemon = db.relationship('User_Pokemon', backref='pokemon', lazy=True)

    def __init__(self, Name, HP, ATK, DEF, SPD, Ability, ImgURL):
        self.Name = Name
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.SPD = SPD
        self.Ability = Ability
        self.ImgURL = ImgURL

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()


class User_Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    user = db.relationship('User', backref='user_pokemon', lazy=True)

    def __init__(self, user_id, pokemon_id):
        self.user_id = user_id
        self.pokemon_id = pokemon_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()