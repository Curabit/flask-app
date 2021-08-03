import pyrebase
from scripts import fbuser
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)

# home route
@app.route("/", methods=['GET','POST'])
def login(isError=False, err=None):
    if request.method == 'POST':
        email = request.form.get('email')
        psw = request.form.get('psw')
        r =  fbuser.sign_in(email, psw)
        if r.status_code!=200:
            resp = r.json()
            msg = resp['error']['message']

            err = dict()
            if msg == 'INVALID_PASSWORD':
                err['headline'] = 'Incorrect Password'
                err['msg'] = 'The password entered did not match with our records. Please try again.'
            elif msg == 'EMAIL_NOT_FOUND':
                err['headline'] = 'Email ID not recognized'
                err['msg'] = 'The email ID entered did not match with any of our user records. Please try again. If you are not registered as a licensed provider with us, please contact us at hello@curabit.in to get yourself registered.'
            elif msg == 'TOO_MANY_ATTEMPTS_TRY_LATER':
                err['headline'] = ''
                err['msg'] = 'Access to this account has been temporarily disabled due to many failed login attempts. You can immediately restore it by resetting your password or you can try again later.'
            elif msg == 'USER_DISABLED':
                err['headline'] = 'User ID disabled'
                err['msg'] = 'Your user account has been disabled. Please contact us at tech-support@curabit.in to re-activate your account.'
            else:
                err['headline'] = msg
                err['msg'] = msg
            
            return render_template('login.html', isError=True, err=err)
        else:
            return jsonify(r.json())
    else:
        return render_template('login.html', isError=False, err=None)

@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')

@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin.html')

def error(msg, code):
    return render_template('Error.html',msg=msg, code=code)

if __name__ == '__main__':
    app.run(debug=True)