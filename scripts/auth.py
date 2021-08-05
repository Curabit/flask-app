import logging, os, requests, json
from flask import render_template, make_response, url_for, redirect, request
from scripts import db, errors

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

web_key = os.environ.get('FIREBASE_WEB_API_KEY')

def set_cookies(authResp, redirect_to='login'):

    logging.debug("Setting cookies")
    resp = make_response()

    logging.debug("Storing user ID")
    if ('localId' in authResp.keys()):
        resp.set_cookie('uId', authResp['localId'])
    elif ('user_id' in authResp.keys()):
        resp.set_cookie('uId', authResp['user_id'])
    
    logging.debug("Storing ID token")
    if ('idToken' in authResp.keys()):
        resp.set_cookie('idToken', authResp['idToken'])
    elif ('id_token' in authResp.keys()):
        resp.set_cookie('idToken', authResp['id_token'])
    
    logging.debug("Storing refresh token")
    if ('refreshToken' in authResp.keys()):
        resp.set_cookie('rToken', authResp['refreshToken'])
    elif ('refresh_token' in authResp.keys()):
        resp.set_cookie('rToken', authResp['refresh_token'])

    if ('uType' not in request.cookies):
        uType = db.check_admin_rights(request.cookies.get('idToken'), request.cookies.get('uId'))

    logging.info("Redirecting to %s", redirect_to)
    resp.headers['location'] = url_for(redirect_to) 

    logging.debug("Returning redirect response with code 302")
    return resp, 302

def refreshToken(rToken, key=web_key):
    api_url = 'https://securetoken.googleapis.com/v1/token'
        
    payload = json.dumps({
        "grant_type": "refresh_token",
        "refresh_token": rToken
    })

    logging.debug("Sending request to refresh token")
    r = requests.post(api_url,
                    params={"key": key},
                    data=payload)
    
    logging.info("Received response: %s", str(r))

    resp = r.json()
    if (r.status_code != 200):
        return errors.handle_error(resp)
    else:
        logging.debug("Setting cookies to newly refreshed auth details")
        set_cookies(resp)
        return 'Cookies refreshed successfully'

def sign_in(email, psw, key=web_key):
    
    api_url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'
        
    payload = json.dumps({
        "email": email,
        "password": psw,
        "returnSecureToken": True
    })

    logging.debug("Sending request to sign in")
    r = requests.post(api_url,
                    params={"key": key},
                    data=payload)
    
    logging.info("Received response: %s", str(r))

    resp = r.json()
    if (r.status_code != 200):
        return errors.handle_error(resp) 

    else:
        
        logging.debug("Setting cookies to newly received auth details")
        set_cookies(resp)

        logging.debug("Redirecting to login page")
        return redirect('login')

def sign_up(email, psw, key=web_key):
    
    api_url = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp'
        
    payload = json.dumps({
        "email": email,
        "password": psw,
        "returnSecureToken": True
    })

    logging.debug("Sending request to sign up")
    r = requests.post(api_url,
                    params={"key": key},
                    data=payload)
    
    logging.info("Received response: %s", str(r))

    resp = r.json()
    if (r.status_code != 200):
        return errors.handle_error(resp) 
        
    else:
        
        logging.debug("Setting cookies to newly received auth details")
        set_cookies(resp)

        logging.debug("Redirecting to login page")
        return redirect('login')
