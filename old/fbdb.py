import os
import logging
import requests

db_url = os.environ.get("FIREBASE_DB_URL")


def check_admin(uid, idToken, db_url=db_url):
        logging.debug("Checking if user is admin")
        endpoint = '/admin-access.json'
        resp = requests.get(db_url+endpoint, params={"auth": idToken}).json()
        logging.info("Received admin check response: "+str(resp))
        if resp[uid] is True:
            logging.info("User found to be admin")
            return 'admin'
        else:
            logging.info("User found to be therapist")
            return 'therapist'

def get_dashboard_details(uid, idToken, db_url=db_url):
    logging.debug("Getting therapist's details")
    endpoint = '/users/'+uid+'.json'
    resp = requests.get(db_url+endpoint, params={"auth": idToken}).json()
    logging.debug("Receiveing therapist's details as: "+str(resp))
    result = dict()
    result['name'] = resp['displayName']
    result['clients'] = list()
    for k,v in resp['clients'].items():
        temp = list()
        temp['clientId'] = k
        temp['clientName'] = v['clientName']
    result['hist'] = ""
    #TODO: Add usage history
    return resp