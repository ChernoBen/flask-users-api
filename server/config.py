import os
import random
import string

import os
import random, string

class Config(object):
    CSRF_ENABLED = True
    SECRET = 'ysb_92=qe#dgjf8%0ng+a*#4rt#5%3*4kw5%i2bck*gn@w3@f&-&'
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + os.getenv('MYSQL_USER') + ':' + os.getenv('MYSQL_ROOT_PASSWORD') + '@localhost:3306/'+ os.getenv('MYSQL_DATABASE')
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///banco.db'
    SENDGRID_API_KEY = 'API_KEY'
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN') if os.getenv('MAILGUN_DOMAIN') else None
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY') if os.getenv('MAILGUN_API_KEY') else None
    FROM_TITLE = 'NO-REPLY'
    FROM_EMAIL = 'no-reply@flaskrestapi.com'


class DevelopmentConfig(Config):
    TESTING = False
    DEBUG = True
    IP_HOST = os.getenv('APIHOST')
    PORT_HOST = os.getenv('APIPORT')
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost' # Aqui geralmente é um IP de um servidor na nuvem e não o endereço da máquina local
    PORT_HOST = 5000
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    IP_HOST = 'localhost' # Aqui geralmente é um IP de um servidor na nuvem e não o endereço da máquina local
    PORT_HOST = 8080
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

app_config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'production': ProductionConfig()
}

app_active = os.getenv('FLASK_ENV')