from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from utils.config import app_active,app_config

config = app_config[app_active]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db',MigrateCommand)

class Role(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),unique=True,nullable=False)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    description = db.Column(db.Text(),nullable=False)

class UserModels(db.Model):
    __tabelname__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(40),unique=True,nullable=True)
    email = db.Column(db.String(120),nullable=False)

class SiteModel(db.Model):
    __tablename__ = 'sites'
    site_id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(80))
    hoteis = db.relationship('hoteis')

class HotelModel(db.Model):
    __tablename__ = 'hoteis'
    hotel_id = db.Column(db.String,primary_key=True)
    nome = db.Column(db.String(80))
    estrelas = db.Column(db.Float(precision=1))
    diaria = db.Column(db.Float(precision=2))
    cidade = db.Column(db.String(40))
    site_id = db.Column(db.Integer,db.ForeignKey('sites.site_id'))

if __name__ == '__main__':
    manager.run()