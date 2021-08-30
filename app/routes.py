from app.mails import ackSignUp, approvedSignUp, notifySignUp
from app import app
from flask import json, url_for, redirect, render_template, flash, request, jsonify
from werkzeug.urls import url_parse
from app.forms import formForgotPassword, formLogin, formRegisterTherapist, formResetPassword
from app.models import User, Client, testJSON, apiObj
from app.api import add_code, get_id, get_user_status
from flask_login import current_user, login_user, logout_user, login_required
import datetime as dt
from threading import Thread
from time import sleep
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if current_user.user_type == 'therapist':
            return redirect(url_for('therapist_db'))
        elif current_user.user_type == 'admin':
            return redirect(url_for('admin_db'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = formLogin()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is None:
            flash('This email ID is not registered.')
            return redirect(url_for('login'))
        elif not (user.check_hash(user,psw=form.psw.data)):
            flash('Invalid password.')
            return redirect(url_for('login'))
        elif not (user.isVerified):
            flash('Your ID has not been verified by Curabit yet.')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            user.log_in()

            # There are actually three possible cases that need to be considered to determine where to redirect after a successful login:

            # - If the login URL does not have a next argument, then the user is redirected to the index page.
            # - If the login URL includes a next argument that is set to a relative path (or in other words, a URL without the domain portion), then the user is redirected to that URL.
            # - If the login URL includes a next argument that is set to a full URL that includes a domain name, then the user is redirected to the index page.

            # The first and second cases are self-explanatory. 
            # The third case is in place to make the application more secure. 
            # An attacker could insert a URL to a malicious site in the next argument, so the application only redirects when the URL is relative, which ensures that the redirect stays within the same site as the application. 
            # To determine if the URL is relative or absolute, I parse it with Werkzeug's url_parse() function and then check if the netloc component is set or not.

            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('login')
            return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = formRegisterTherapist()
    if form.validate_on_submit():
        user = User(
            email = form.email.data,
            name = form.th_name.data,
            user_details = {
                'clinic_name': form.clinic_name.data,
                'clinic_add': form.clinic_add.data
            },
            psw = form.psw.data
        )
        user.save()
        ackSignUp(email=form.email.data, th_name=form.th_name.data)
        notifySignUp(name=form.th_name.data, email=form.email.data, cl_name=form.clinic_name.data, cl_add=form.clinic_add.data)
        flash("Your details will now be verified by Curabit. We'll send you an email when your account is ready.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = formForgotPassword()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        print("NAME: "+str(user.name))
        if user is None:
            flash('This email ID is not registered.')
            return redirect(url_for('forgotPassword'))
        else:
            user.send_reset_email()
            flash('An email has been sent to you with instructions on how to reset your password.')
            return redirect(url_for('login'))
    return render_template('forgot_psw.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid token or token expired.')
        return redirect(url_for('login'))
    form = formResetPassword()
    if form.validate_on_submit():
        user.set_hash(form.new_psw.data)
        user.save()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_psw.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.')
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_db():
    th_list = User.objects(user_type='therapist')
    return render_template('admin_db.html', ths=th_list)

@app.route('/admin/reset_link', methods=['GET'])
@login_required
def admin_reset_link():
    if current_user.user_type!='admin':
        return redirect(url_for('index'))
    user = User.objects(_id=request.args.get('user_id')).first()
    if user is None:
        flash("Could not find therapist.")
    else:
        user.send_reset_email()
        flash('Password Reset Instructions have been mailed.')
    return redirect(url_for(request.args.get('redirect_to')))

@app.route('/admin/approve', methods=['GET'])
@login_required
def admin_approve():
    if current_user.user_type!='admin':
        return redirect(url_for('index'))
    user = User.objects(_id=request.args.get('user_id')).first()
    if user is None:
        flash("Could not find therapist.")
    else:
        user.update(isVerified=True)
        flash(user.name+" has been approved.")
    return redirect(url_for(request.args.get('redirect_to')))

@app.route('/admin/disapprove', methods=['GET'])
@login_required
def admin_disapprove():
    if current_user.user_type!='admin':
        return redirect(url_for('index'))
    user = User.objects(_id=request.args.get('user_id')).first()
    if user is None:
        flash("Could not find therapist.")
    else:
        user.update(isVerified=False)
        approvedSignUp(user.email, user.name)
        flash(user.name+"'s approval has been revoked.")
    return redirect(url_for(request.args.get('redirect_to')))

@app.route('/admin/delete', methods=['GET'])
@login_required
def admin_delete():
    if current_user.user_type!='admin':
        return redirect(url_for('index'))
    user = User.objects(_id=request.args.get('user_id')).first()
    if user is None:
        flash("Could not find therapist.")
    else:
        #TODO: Add confirmation dialog for deletion
        flash("You cannot afford to delete therapists right now. Scale up, then we'll talk.")
    return redirect(url_for(request.args.get('redirect_to')))


@app.route('/therapist', methods=['GET', 'POST'])
@login_required
def therapist_db():
    cls = Client.objects(th_id=current_user._id)
    return render_template('therapist_db.html', cls=cls)

@app.route('/therapist/add_client', methods=['POST'])
@login_required
def add_client():
    if current_user.user_type!='therapist':
        return redirect(url_for('index'))
    client = Client(th_id=current_user._id, 
    name=request.form.get('name'),
    age=request.form.get('age'),
    sex=request.form.get('sex'))
    client.save()
    flash('Client added successfully.')
    return redirect(url_for('therapist_db'))

@app.route("/api/json", methods=["PUT"])
def serve_json():
    if request.method=="POST":
        test_obj = testJSON.objects().first()
        if test_obj is not None:
            test_obj.delete()
        body = request.get_json()
        test_obj = testJSON(**body).save()
        return jsonify(test_obj), 201
    else:
        test_obj = testJSON.objects().first()
        return jsonify(test_obj), 200

@app.route('/api/endpoint', methods=['PUT'])
def handle_api_req():
    try:
        req = request.get_json(force=True)
        req_type = req['req']
        if req_type=="set_pairing_code":
            return add_code(req['code'])
        elif req_type=='get_id':
            return get_id(req['code'])
        elif req_type=='get_user_session':
            return get_user_status(req['id'])
        else:
            return jsonify({"resp": "Operation not found."}), 400
    except Exception as e:
        return jsonify({
            "resp": "Error",
            "msg": str(e)
        }), 400
    


        
    
@app.route('/therapist/pair_headset', methods=['POST'])
@login_required
def pair_headset():
    code = request.form.get('code')
    token = apiObj.objects(
        req='set_pairing_code',
        code=code
        ).first()
    if token is not None:
        current_user.update(hcode=code)
        token.delete()
        flash('Paired headset successfully.')
    else:
        flash('Pairing code expired or invalid.')
    return redirect(request.referrer)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update(lastActivity=datetime.utcnow())

@app.template_filter()
def format_datetime(value):
    ist_diff = dt.timedelta(hours=5, minutes=30)
    ist_time = value + ist_diff
    return ist_time.strftime("%d %B, %Y, %-I:%M:%S %p")
