from scripts import auth, db, errors
from flask import Flask, render_template, request, jsonify, redirect,url_for, Response, make_response
import logging

app = Flask(__name__)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

def verify_role(match_type=None, redirect_to='login'):
    logging.debug("Checking cookies for user type")
    if ('uType' not in request.cookies):
        logging.debug("No cookies found")
        return render_template(str(redirect_to+'.html'), isError=False, err=None)
    else:
        logging.debug("Found cookies")
        uType = request.cookies.get('uType')
        if match_type == uType:
            return "All OK"
        else:
            if uType == 'admin':
                logging.debug("User identified as admin")
                return redirect(url_for('admin'))
            else:
                logging.debug("User identified as therapist")
                return redirect(url_for('therapist'))

@app.route("/", methods=['GET','POST'])
@app.route("/login", methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        
        logging.debug("Accessing / via POST method")
        email = request.form.get('email')
        psw = request.form.get('psw')
        
        logging.debug("Signing In")
        return auth.sign_in(email, psw)
        
    else:
        logging.debug("Accessing / via GET method")
        return verify_role()

@app.route("/admin/dashboard", methods=['GET'])
def admin():

    chk_role = verify_role('admin')
    if chk_role != "All OK":
        return chk_role

    return render_template('admin.html')

@app.route("/admin/add", methods=['GET', 'POST'])
def add_therapist():
    
    # Registration of therapist from admin's console
    if request.method == 'POST':
        
        logging.debug("Accessing / via POST method")
        email = request.form.get('email')
        psw = request.form.get('psw')
        name = request.form.get('name')
        clinic = dict()
        clinic['name'] = request.form.get('clinic_name')
        clinic['address'] = request.form.get('clinic_add')
        
        logging.debug("Signing up")
        return auth.sign_up(email=email, psw=psw, name=name, clinic=clinic)
        
    else:
        logging.debug("Accessing / via GET method")
        return render_template('register.html')

@app.route("/admin/reset-password", methods=['GET', 'POST'])
def reset_password():
    pass
    #TODO: Reset password from admin's console

@app.route("/admin/view-logs", methods=['GET', 'POST'])
def view_logs():
    pass
    #TODO: View logs from admin's console

@app.route("/therapist/dashboard", methods=['GET'])
def therapist():
    
    chk_role = verify_role('therapist')
    if chk_role != "All OK":
        return chk_role
    
    return render_template('dashboard.html')

@app.route("/therapist/client/view", methods=['GET', 'POST'])
def view_client():
    pass
    #TODO: View client's details

@app.route("/therapist/client/add", methods=['GET', 'POST'])
def add_client():
    pass
    #TODO: Addition of client by therapist

@app.route("/therapist/client/delete", methods=['GET', 'POST'])
def delete_client():
    pass
    #TODO: Add Javascript alert that confirm's deletion of client
    #TODO: Delete client from therapist's console

@app.route("/therapist/session/view", methods=['GET', 'POST'])
def view_session():
    pass
    #TODO: View session's details

@app.route("/therapist/session/do", methods=['GET', 'POST'])
def do_session():
    pass
    #TODO: Do session

@app.route("/therapist/session/stop", methods=['GET', 'POST'])
def stop_session():
    pass
    #TODO: Stop session

@app.route("/action/logout", methods=['GET','POST'])
def logout():
    return auth.clear_cookies()

#Error Handling
@app.errorhandler(errors.AuthError)
def auth_error(e):
    return render_template('login.html', isError=True, err=e.msg)

@app.errorhandler(errors.UnknownError)
def unknown_error(e):
    return render_template('error.html',msg=e.msg, code=e.code)

# Test Routes
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

@app.route("/api/test/get-json", methods=['GET','POST'])
def test_get_json():
    data = {
    'isStop': False,
	'current': {
		'file-name': 'current-video.mp4',
		'isOnLoop': True
		},
    'next-count': 3,
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
