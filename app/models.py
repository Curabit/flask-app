import random
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login
from time import time
from app import app
from werkzeug.exceptions import Forbidden
from app.mails import resetPass
import jwt


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    _id = db.StringField(primary_key=True, 
    default=''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)]))
    email = db.StringField(required=True)
    psw_hash = db.StringField(required=True)
    name = db.StringField(required=True)
    user_type = db.StringField(required=True, default="therapist")
    user_details = db.DynamicField()
    isVerified = db.BooleanField(required=True, default=False)
    lastActivity = db.DateTimeField()
    created_at = db.DateTimeField(required=True, default=datetime.utcnow())

    def __init__(self, psw=None, *args, **values):
        super().__init__(*args, **values)
        if psw is not None:
            self.set_hash(psw)
    
    def log_in(self):
        self.lastLoggedIn = datetime.utcnow()

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_anonymous():
        return False

    def get_id(self):
        return self._id

    def set_hash(self, psw):
        self.psw_hash = generate_password_hash(psw)

    @staticmethod
    def check_hash(self, psw):
        return check_password_hash(self.psw_hash, psw)
    
    def get_reset_password_token(self, expires_in=600):
        x = jwt.encode(
            {'reset_password': self._id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
        print(x)
        return x

    def send_reset_email(self):
        resetPass(email=self.email, th_name=self.name, token=self.get_reset_password_token())

    @staticmethod
    def verify_reset_password_token(token):
        try:
            resp = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])
            _id = resp['reset_password']
        except Exception as e:
            return
        return User.objects(_id=_id).first()

class Client(db.Document):
    meta = {"collection": "clients"}
    _id = db.StringField(primary_key=True)
    th_id = db.StringField(required=True)
    name = db.StringField(required=True)
    age = db.IntField()
    sex = db.StringField(required=True)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self._id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])

class Scene(db.Document):
    meta = {"collection": "scenes"}
    _id = db.StringField(primary_key=True)
    name = db.StringField(required=True)
    flow = db.DynamicField(required=True)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self._id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])

class Session(db.Document):
    meta = {"collections": "sessions"}
    _id = db.StringField(primary_key=True)
    th_id = db.StringField(required=True)
    cl_id = db.StringField(required=True)
    sc_id = db.StringField(required=True)
    beganAt = db.DateTimeField(required=True, default=datetime.utcnow())
    endAt = db.DateTimeField(required=True)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self._id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])

@login.user_loader
def load_user(_id):
    return User.objects(pk=_id).first()
