from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from sendgrid import SendGridAPIClient
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
sg = SendGridAPIClient(app.config['SENDGRID_API_KEY'])
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, mails, errors, forms