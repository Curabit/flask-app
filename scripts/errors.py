import logging
from flask import render_template

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

auth_errors = {
    "INVALID_PASSWORD": {
        "headline": "Incorrect Password",
        "msg": "The password entered did not match with our records. Please try again."
    },
    "EMAIL_NOT_FOUND": {
        "headline": "Email ID not recognized",
        "msg": "The email ID entered did not match with any of our user records. Please try again. If you are not registered as a licensed provider with us, please contact us at hello@curabit.in to get yourself registered."
    },
    "TOO_MANY_ATTEMPTS_TRY_LATER": {
        "headline": "You have tried too many times.",
        "msg": "Access to this account has been temporarily disabled due to many failed login attempts. You can immediately restore it by resetting your password or you can try again later."
    },
    "USER_DISABLED": {
        "headline": "User ID disabled",
        "msg": "Your user account has been disabled. Please contact us at tech-support@curabit.in to re-activate your account."
    },
    "TOKEN_EXPIRED": {
        "headline": "Your session has expired.",
        "msg": "Please login again."
    },
    "USER_NOT_FOUND": {
        "headline": "Your user details could not be found.",
        "msg": "Your credentials cannot be verified. Please login again."
    },
    "INVALID_REFRESH_TOKEN": {
        "headline": "Your session has expired.",
        "msg": "Please login again."
    },
    "INVALID_GRANT_TYPE": {
        "headline": "Your session has expired.",
        "msg": "Please login again."
    },
    "MISSING_REFRESH_TOKEN": {
        "headline": "Your session has expired.",
        "msg": "Please login again."
    }
}

class AuthError(Exception):    
    def __init__(self, resp):
        logging.debug("Authentication Error. Rendering login page with error details.")
        self.msg = auth_errors[resp['error']['message']]

class UnknownError(Exception):
    def __init__(self, resp):
        logging.warning("Unknown error from Firebase Auth API. Rendering error page with details.")
        self.code = resp['error']['code']
        self.msg = str(resp)

def handle_error(resp):

    if (resp['error']['message'] in auth_errors):
        raise AuthError(resp)
    else:
        raise UnknownError(resp)