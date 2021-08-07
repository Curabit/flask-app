import datetime
import logging, os, requests, json
from flask.json import jsonify
from flask import render_template, make_response, url_for, redirect, request
from scripts import errors

db_url = os.environ.get("FIREBASE_DB_URL")

def check_admin_rights(idToken, uid):
    
    logging.debug("Checking if user is admin")
    # logging.info("idToken: %s", idToken)
    endpoint = '/admin-access.json'
    r = requests.get(db_url+endpoint, params={"auth": idToken})
    logging.info("Received response: "+str(r.json()))

    if (r.status_code != 200):
        errors.handle_error(r.json())
    else:
        resp = r.json()
        if resp[uid] is True:
            logging.info("User found to be admin")
            return 'admin'
        else:
            logging.info("User found to be therapist")
            return 'therapist'

def add_therapist(email, uId, name, clinic, idToken=request.cookies.get('idToken'), db_url=db_url):

    logging.debug("Setting admin privileges to read-only")
    endpoint = '/admin-access.json'
    payload = {
        uId:False
    }
    r = requests.post(db_url+endpoint, data={"auth": idToken}, json=jsonify(payload))
    logging.info("Received response: "+str(r.json()))
    if (r.status_code != 200):
        errors.handle_error(r.json())

    logging.debug("Pushing new therapist's data to db")
    endpoint = "/users.json"
    payload = {
        uId: {
            'clients': [],
            'history': [],
            'name': name,
            'email': email,
            'clinic': clinic,
            'registered': datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        }
    }
    r = requests.post(db_url+endpoint, data={"auth": idToken}, json=jsonify(payload))
    logging.info("Received response: "+str(r.json()))

    if (r.status_code != 200):
        errors.handle_error(r.json())

    
