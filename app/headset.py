from werkzeug.exceptions import NotFound
from app.models import obj
from flask_login import current_user

def add_headset(code):

    req = obj.objects(req='start_pair',code=code).first()
    if req is not None:
        req=obj(req='ack_pair', code=code, _id=current_user._id)
        req.save()