import logging, os, requests, json
from flask import render_template, make_response, url_for, redirect
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