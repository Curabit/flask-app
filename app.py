from scripts import fbuser, errors, db, auth, fbdb
from flask import Flask, render_template, request, jsonify, redirect,url_for, Response, make_response
import logging

app = Flask(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

class TestError(Exception):
    def __init__(self):
        self.code = 400
        self.msg = "I created this error"

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
        
        logging.debug("Checking cookies for user type")
        if not request.cookies.get('uType'):
            logging.debug("No cookies found")
            return render_template('login.html', isError=False, err=None)
        else:
            uType = request.cookies.get('uType')
            if uType == 'admin':
                logging.debug("Found admin user cookies")
                return redirect(url_for('admin'))
            else:
                logging.debug("Found non-admin user cookies")
                return redirect(url_for('dashboard'))

@app.route("/register", methods=['GET'])
def register():
    return render_template('register.html')

@app.route("/admin", methods=['GET'])
def admin():

    logging.debug("Checking cookies for user type")
    if not request.cookies.get('uType'):
        logging.debug("No cookies found")
        return redirect(url_for('login'))
    else:
        uType = request.cookies.get('uType')
        if uType != 'admin':
            logging.debug("Found non-admin user cookies. Redirecting to user dashboard.")
            return redirect(url_for('dashboard'))

    email = request.cookies.get('email')
    return render_template('admin.html', email=email)

@app.route("/dashboard", methods=['GET'])
def dashboard():
    
    logging.debug("Checking cookies for user type")
    if not request.cookies.get('uType'):
        logging.debug("No cookies found")
        return redirect(url_for('login'))
    else:
        uType = request.cookies.get('uType')
        if uType == 'admin':
            logging.debug("Found admin user cookies. Redirecting to admin console.")
            return redirect(url_for('admin'))
    
    return render_template('dashboard.html')

@app.route("/action/logout", methods=['GET','POST'])
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie(key='dispName')
    resp.delete_cookie(key='email')
    resp.delete_cookie(key='session-validity')
    resp.delete_cookie(key='idToken')
    resp.delete_cookie(key='refreshToken')
    resp.delete_cookie(key='uType')
    return resp

@app.route("/test/dashboard", methods=['GET','POST'])
def test_dashboard():
    pack = dict()
    pack['dispName'] = 'Test User'
    return render_template('dashboard.html', pack=pack)

@app.route("/test/client", methods=['GET','POST'])
def test_client():
    pack = dict()
    pack['clientName'] = 'Test User'
    return render_template('client.html', pack=pack)

@app.route("/action/register", methods=['POST'])
def signup():
    pass

@app.errorhandler(TestError)
def test_error_handler(e):
    return render_template('error.html', msg=e.msg, code=e.code), 400

@app.route("/test/error", methods=['GET','POST'])
def test_error():
    raise TestError

@app.route("/api/test/get-json", methods=['GET','POST'])
def test_get_json():
    data = {
	'current': {
		'file-name': 'current-video.mp4',
		'isOnLoop': True
		},
	'next': [{
		'file-name': 'next-video-1.mp4',
		'isOnLoop': True
		},
		{
		'file-name': 'next-video-2.mp4',
		'isOnLoop': False
		},
		{
		'file-name': 'next-video-3.mp4',
		'isOnLoop': False
		}],
	'previous': {
		'file-name': 'previous-video.mp4',
		'isOnLoop': False
		}
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
