from flask import jsonify
from app.models import User, apiObj
from threading import Thread
from time import sleep

def delete_temp_apiObj(code):
    sleep(600)
    token = apiObj.objects(
        req='set_pairing_code',
        code=code
        ).first()
    if token is not None:
        token.delete()

def add_code(code):
    user = User.objects(hcode=code).first()
    token = apiObj(code=code).first()
    if user is None and token is None:
        token = apiObj(
            req='set_pairing_code',
            code=code
        ).save()
        Thread(target=delete_temp_apiObj, args=(token,)).start()
        return jsonify({"resp": "OK"}), 201
    else:
        return jsonify({"resp": "Code already exists"}), 400

def get_id(code):
    user = User.objects(hcode=code).first()
    if user is not None:
        return jsonify({"resp": user._id}), 200
    else:
        return jsonify({'resp': 'Code not paired yet.'}), 400

def get_user_status(_id):
    user = User.objects(pk=_id).first()
    if user is not None:
        return jsonify({
            'resp': 'OK',
            'session_details': user.session
        }), 200
    else:
        return jsonify({
            'resp': 'User not found.'
        }), 400