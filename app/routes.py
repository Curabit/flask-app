from flask import render_template, flash, redirect, jsonify, url_for, request
from app import app
from datetime import datetime
from app.forms import LoginForm, RegisterForm, ForgotPasswordForm, newClient, editDetailsForm
from app.models import User, Client, testJSON
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.register(th_name=form.th_name.data, clinic_name=form.clinic_name.data, clinic_add=form.clinic_add.data, email=form.email.data)
        user.set_hash(psw=form.psw.data)
        user.save()
        flash('Your details will now be verified by Curabit. We send you an email when your account is ready.')
        # login_user(user)
        return redirect(url_for('login'))
    return render_template('register-new.html', form=form)

@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if (user is None):
            flash('Email ID not registered.')
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
                next_page = url_for('dashboard')
                return redirect(next_page)
            else:
                return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/forgot-password', methods=["GET", "POST"])
def forgotpsw():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            flash("An email has been sent to the given email ID.")
            return redirect(url_for('login'))
        return render_template("forgotpsw.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    clients = Client.objects(th_id=current_user._id)
    return render_template('dashboard.html', clients=clients)

@app.route('/view-account')
@login_required
def view_account():
    return render_template('account-view.html')

@app.route('/add-client', methods=["GET", "POST"])
@login_required
def add_client():
    form = newClient()
    if form.validate_on_submit():
        client = Client()
        client.register(th_id=current_user._id, clnt_name=form.clnt_name.data, gender=form.gender.data, age=form.age.data)
        client.save()
        return redirect(url_for('dashboard'))
    return render_template('add-client.html', form=form)

@app.route('/edit-account', methods=["GET", "POST"])
@login_required
def edit_account():
    form = editDetailsForm()
    if form.validate_on_submit():
        current_user.update(th_name = form.th_name.data, clinic_name = form.clinic_name.data, clinic_add = form.clinic_add.data, email=form.email.data)
        return redirect(url_for('view_account'))
    form.th_name.data = current_user.th_name
    form.clinic_name.data = current_user.clinic_name
    form.clinic_add.data = current_user.clinic_add
    form.email.data = current_user.email
    return render_template('account-edit.html', form=form)

@app.route('/view-client/<clientId>')
@login_required
def view_client(clientId):
    client = Client.objects(_id=clientId).first()
    if client.th_id!=current_user._id:
        flash("You cannot access this client.")
        redirect(url_for('dashboard'))
    return render_template('client-view.html', client=client)

@app.route("/api/json", methods=["POST","GET"])
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


# @app.route("/api/test/get-json", methods=['GET','POST'])
# def test_get_json():
    # data = {
    # 'isStop': False,
	# 'current': {
	# 	'file-name': 'current-video',
	# 	'isOnLoop': True
	# 	},
    # 'total-count': 4,
    # 'next': [{
	# 	'file-name': 'next-video-1',
	# 	'isOnLoop': True
	# 	},
	# 	{
	# 	'file-name': 'next-video-2',
	# 	'isOnLoop': False
	# 	},
	# 	{
	# 	'file-name': 'next-video-3',
	# 	'isOnLoop': False
	# 	}],
	# 'previous': {
	# 	'file-name': 'previous-video',
	# 	'isOnLoop': False
	# 	}
    # }
#     return jsonify(data)