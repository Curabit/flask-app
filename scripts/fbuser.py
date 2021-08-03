import os
import json
import requests

web_key = os.environ.get('FIREBASE_WEB_API_KEY')

def sign_in(email, psw, key=web_key, isTokenSecure=True):
    api_url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword'
    
    if email is None:
        return "No email specified", 400
    elif psw is None:
        return "No password specified", 400
    
    payload = json.dumps({
        "email": email,
        "password": psw,
        "returnSecureToken": isTokenSecure
    })

    r = requests.post(api_url,
                      params={"key": key},
                      data=payload)
    
    return r