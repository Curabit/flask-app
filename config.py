import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGODB_SETTINGS = {
        'db': 'curabit-app',
        'host': os.environ.get('MONGO_URI')
    }
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')