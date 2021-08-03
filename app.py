from scripts import fbuser
from flask import Flask, render_template, request
import logging

app = Flask(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

# home route
@app.route("/", methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        
        logging.debug("Accessing / via POST method")
        email = request.form.get('email')
        psw = request.form.get('psw')
        
        logging.debug("Signing In")
        r =  fbuser.sign_in(email, psw)
        
        logging.info("Type of returned object: %s", str(type(r)))
        if isinstance(r, fbuser.userObj):
            logging.debug("Found userObj returned as object")

            if r.uType == 'admin':
                logging.debug("Setting cookie and redirecting to admin's console")
                return r.set_cookie(redirect_to='admin')
            else:
                logging.debug("Setting cookie and redirecting to therapist's dashboard")
                return  r.set_cookie(redirect_to='dashboard')
        else:
            logging.debug("Found render_template() as returned object")
            return r
    else:
        logging.debug("Accessing / via GET method")
        return render_template('login.html', isError=False, err=None)

@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')

@app.route("/admin", methods=['GET'])
def admin():
    email = request.cookies.get('email')  
    return render_template('admin.html', email=email)

@app.route("/dashboard", methods=['GET'])
def dashboard():
    return render_template('dashboard.html')
    

if __name__ == '__main__':
    app.run(debug=True)