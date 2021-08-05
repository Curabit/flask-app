import logging, os, requests, json
from flask import render_template, make_response, url_for, redirect
from scripts import errors

db_url = os.environ.get("FIREBASE_DB_URL")

# def check_resp_errors(resp):



def check_admin_rights(idToken, uid):
    
    logging.debug("Checking if user is admin")
    endpoint = '/admin-access.json'
    r = requests.get(db_url+endpoint, params={"auth": idToken})
    logging.info("Received admin check response: "+str(r))

    if (r.status_code != 200):
        return errors.handle_error(r.json())
    else:
        resp = r.json()
        if resp[uid] is True:
            logging.info("User found to be admin")
            return 'admin'
        else:
            logging.info("User found to be therapist")
            return 'therapist'