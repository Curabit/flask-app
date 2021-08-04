import os
import json
import requests
import datetime
from flask import render_template, make_response, url_for, request

import logging

from werkzeug.utils import redirect

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

web_key = os.environ.get('FIREBASE_WEB_API_KEY')
db_url = os.environ.get("FIREBASE_DB_URL")

class userObj:

    def __init__(self):
        logging.debug("Creating User Object")
        self.dispName = ""
        self.email = ""
        self.uType = ""
        self.token = dict()
        
    def check_admin(self, email, db_url=db_url):
        logging.debug("Checking if user is admin")
        endpoint = '/admin-access.json'
        resp = requests.get(db_url+endpoint).json()
        
        if email in resp:
            logging.info("User found to be admin")
            return 'admin'
        else:
            logging.info("User found to be therapist")
            return 'therapist'
    
    def setToken(self, r):
        logging.debug("Setting token from received response.")
        self.token['idToken'] = r['idToken']
        self.token['refreshToken'] = r['refreshToken']
        self.token['expiry'] = datetime.datetime.now()+datetime.timedelta(seconds=int(r['expiresIn']))
        self.token['expiry'] = self.token['expiry'].strftime("%m/%d/%Y, %H:%M:%S")
        # read as date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
    
    def setDetails(self, r):
        logging.debug("Setting user details from received response.")
        self.dispName = r['displayName']
        self.email = r['email']
        self.uType = self.check_admin(self.email,db_url=db_url)

    def set_cookie(self, redirect_to):

        logging.debug("Setting cookies")
        resp = make_response()

        resp.set_cookie('dispName',self.dispName)
        resp.set_cookie('email',self.email)
        resp.set_cookie('session-validity',self.token['expiry'])
        resp.set_cookie('idToken',self.token['idToken'])
        resp.set_cookie('refreshToken',self.token['refreshToken'])
        resp.set_cookie('uType',self.uType)

        logging.info("Redirecting to %s", redirect_to)
        resp.headers['location'] = url_for(redirect_to) 

        logging.debug("Returning redirect response with code 302")
        return resp, 302

    # def check_session(self):
    #     if not request.cookies.get('expiry'):
    #         return redirect(url_for('login'))
    #     else:
    #         expiry = datetime.datetime.strptime(str(request.cookies.get('expiry')), '%d/%m/%y %H:%M:%S')
    #         if datetime.datetime.now() > expiry:
    #             return self.refresh_session(request.cookies.get('refreshToken'))
    #         else:
    #             return True

    # def refresh_session(self, rToken, key=web_key):
    #     api_url = 'https://securetoken.googleapis.com/v1/token'
        
    #     payload = json.dumps({
    #         "grant_type": "refresh_token",
    #         "refresh_token": rToken
    #     })

    #     logging.debug("Sending refresh_token request to firebase")
    #     r = requests.post(api_url,
    #                     params={"key": key},
    #                     data=payload)

    #     logging.info("Received response: %s", str(r))

    #     if r.status_code!=200:
            
    #         r_json = r.json()
    #         err_msg = r_json['error']['message']
    #         with open('scripts/errors.json') as errorFile:
    #             err_dict = json.load(errorFile) 
    #         if err_msg in err_dict:
    #             logging.debug("Found familiar error message. Rendering login page once again.")
    #             return render_template('login.html', isError=True, err=err_dict[err_msg])
    #         else:
    #             logging.debug("Found unfamiliar error message. Rendering error page.")
    #             return render_template('error.html',msg=str(r), code=r.status_code)
    #     else:
    #         self.setToken(r.json())
    #         return True
        



def sign_in(email, psw, isTokenSecure=True, key=web_key):
        api_url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'
        
        payload = json.dumps({
            "email": email,
            "password": psw,
            "returnSecureToken": isTokenSecure
        })

        logging.debug("Sending login request to firebase")
        r = requests.post(api_url,
                        params={"key": key},
                        data=payload)
        logging.info("Received response: %s", str(r))

        if r.status_code!=200:
            
            r_json = r.json()
            err_msg = r_json['error']['message']
            with open('scripts/errors.json') as errorFile:
                err_dict = json.load(errorFile) 
            if err_msg in err_dict:
                logging.debug("Found familiar error message. Rendering login page once again.")
                return render_template('login.html', isError=True, err=err_dict[err_msg])
            else:
                logging.debug("Found unfamiliar error message. Rendering error page.")
                return render_template('error.html',msg=str(r.json()), code=r.status_code)
        else:

            user = userObj()
            user.setDetails(r.json())
            user.setToken(r.json())
        
            return user