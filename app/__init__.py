from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from sendgrid import SendGridAPIClient
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
sg = SendGridAPIClient(app.config['SENDGRID_API_KEY'])
login = LoginManager(app)
login.login_view = 'login'


if (os.environ.get('FLASK_ENV') == 'development'):
    from app import routes, models, mails, forms, api
else:
    from app import routes, models, mails, errors, forms, api