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

class UserModels(db.Model):
    __tabelname__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(40),unique=True,nullable=True)
    email = db.Column(db.String(120),nullable=False)


if __name__ == '__main__':
    manager.run()