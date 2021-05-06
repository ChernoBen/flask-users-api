from flask import request,url_for
from utils.sql_alchemy import banco
#from flask_sqlalchemy import SQLAlchemy
from config import app_active,app_config
from requests import post

config = app_config[app_active]
#banco = SQLAlchemy(config.APP)

class UserModel(banco.Model):
    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer,primary_key=True,autoincrement=True)
    email = banco.Column(banco.String(100),nullable=False,unique=True)
    password = banco.Column(banco.String(120),nullable=False,unique=True)
    ativado = banco.Column(banco.Boolean,default=True,nullable=True)

    def __init__(self,email,password,ativado=True):
        self.email = email
        self.password = password
        self.ativado = ativado
    def json(self):
        return {
            'id':self.user_id,
            'email':self.email
        }

    def send_email_confirmation(self):

        link = request.url_root[:-1] + url_for('userconfirm',user_id=self.user_id)
        return post(f"https://api.mailgun.net/v3/{config.YOUR_DOMAIN_NAME}/messages",auth=('api',config.MAILGUN_API_KEY),
                    data={
                        'form':f'{config.FROM_TITLE}<{config.FROM_EMAIL}',
                        'to':self.email,
                        'subject':'Confirmação de email',
                        'text':f'Confirme seu cadastro:{link}',
                        'html':f"<html><p>Confirme seu cadastro pelo link: <a href='{link}'>CONFIRMAR</a></p></html>"
                        }
                    )

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls,email):
        user = cls.query.filter_by(email=email).first()
        print(user,'aqui está o user')
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def update_user(self,email):
        self.email = email

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()