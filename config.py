import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'curabit'
    MONGODB_SETTINGS = {
        'db': 'curabit-app',
        'host': os.environ.get('MONGO_URI')
    }