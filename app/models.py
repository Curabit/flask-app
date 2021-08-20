import random
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(db.Document):
    meta = {'collection': 'users'}
    _id = db.StringField(primary_key=True)
    email = db.StringField(required=True)
    psw_hash = db.StringField(required=True)
    name = db.StringField(required=True)
    user_type = db.StringField(required=True, default="therapist")
    isVerified = db.BooleanField(required=True, default=False)
    lastLoggedIn = db.DateTimeField()
    created_at = db.DateTimeField(required=True, default=datetime.utcnow())

    def set_hash(self, psw):
        self.psw_hash = generate_password_hash(psw)

    @staticmethod
    def check_hash(self, psw):
        return check_password_hash(self.psw_hash, psw)
        
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        self._id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
        self.psw_hash = self.set_hash(args['psw'])

class Therapist(db.Document):
    meta = {"collection": "therapists"}
    _id = db.StringField(primary_key=True)
    clinic_name = db.StringField(required=True)
    clinic_add = db.StringField(required=True)
    #TODO: Add a field for scanned document's PDF

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


