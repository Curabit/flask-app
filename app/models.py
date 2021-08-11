import random
import string
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

from app import db

class User(UserMixin, db.Document):
    meta = {'collection': 'Users'}
    _id = db.StringField(primary_key=True)
    regDate = db.StringField(required=True)
    th_name = db.StringField(required=True)
    clinic_name = db.StringField()
    clinic_add = db.StringField()
    email = db.StringField(required=True)
    lastLoggedIn = db.StringField(required=True)
    psw_hash = db.StringField(required=True)

    def register(self, th_name, clinic_name, clinic_add, email, id=None):
        if id is None:
            self._id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
        else:
            self._id = id
        self.th_name = th_name
        self.clinic_name = clinic_name
        self.clinic_add = clinic_add
        self.email = email
        self.regDate = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        self.lastLoggedIn = self.regDate[:]

    def log_in(self):
        self.lastLoggedIn = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

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

@login.user_loader
def load_user(_id):
    return User.objects(pk=_id).first()