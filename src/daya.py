from flask import Flask, Blueprint
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.bcrypt import Bcrypt
from flask_wtf.csrf import CsrfProtect
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {'HOST': '192.168.100.64', 'DB': 'daya'}
app.config['SECRET_KEY'] = 'DAYA_SECRET_KEY'

db = MongoEngine(app)  # connect MongoEngine with Flask App
app.session_interface = MongoEngineSessionInterface(db)  # sessions w/ mongoengine
# Use the fixer
app.wsgi_app = ProxyFix(app.wsgi_app)

# Flask BCrypt will be used to salt the user password
flask_bcrypt = Bcrypt(app)

# Associate Flask-Login manager with current app
login_manager = LoginManager()
login_manager.init_app(app)

csrf = CsrfProtect()
csrf.init_app(app)

