from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from controllers.user import User,UserRegister,UserLogin,UserLogout,UserConfirm
from flask_jwt_extended import JWTManager
from utils.blocklist import BLOCKLIST
from config import app_config, app_active
from utils.sql_alchemy import banco as db
config = app_config[app_active]

def create_app(config_name):
    print(config.SQLALCHEMY_DATABASE_URI)
    app = Flask(__name__)
    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = config.SECRET
    #db = SQLAlchemy(config.APP)
    db.init_app(app)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    api = Api(app)
    jwt = JWTManager(app)

    @app.before_request
    def cria_banco():
        db.create_all()

    @jwt.token_in_blocklist_loader
    def blocklist_verify(self,token):
        return token['jti'] in BLOCKLIST

    @jwt.revoked_token_loader
    def invalidate_access_token(jwt_headers,jwt_payload):
        return jsonify({'message':'You have been logged out'}),401 #Unauthorized

    api.add_resource(User,'/user/<int:user_id>')
    api.add_resource(UserRegister,'/cadastro')
    api.add_resource(UserLogin,'/login')
    api.add_resource(UserLogout,'/logout')
    api.add_resource(UserConfirm,'/confirm')

    return app