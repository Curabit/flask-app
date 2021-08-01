import pyrebase
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Firebase Setup
config = {
    "apiKey": "AIzaSyDcBsaSLhOdnykdrdoyQYqaYk4zlAIwcrM",
    "authDomain": "curabit.firebaseapp.com",
    "projectId": "curabit",
    "storageBucket": "curabit.appspot.com",
    "messagingSenderId": "877388556031",
    "appId": "1:877388556031:web:f918e32d26f4bfbeaa0eca",
    "measurementId": "G-0Z9H385PXR",
    "serviceAccount": "firebase-admin.json",
    "databaseURL": "",
}
firebase = pyrebase.initialize_app(config)


# home route
@app.route("/", methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')

@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route("/api/login", methods=['GET','POST'])
def api_login():
    
    auth = firebase.auth()
    
    email = request.form.get('email')
    password = request.form.get('psw')
    if email is None or password is None:
        return error('Error missing email or password',400)
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return error('There was an error logging in', 400)

def error(msg, code):
    return render_template('Error.html',msg=msg, code=code)


if __name__ == '__main__':
    app.run(debug=True)