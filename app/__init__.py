from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from sendgrid import SendGridAPIClient

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)
sg = SendGridAPIClient(app.config['SENDGRID_API_KEY'])

from app import routes, models