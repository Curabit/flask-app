from flask import render_template, flash, redirect, jsonify, url_for, request
from app import app
from app.forms import LoginForm, RegisterForm, ForgotPasswordForm, newClient
from app.models import User, Client
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/dashboard')
@login_required
def dashboard():
    clients = Client.objects(th_id=current_user._id)
    return render_template('dashboard.html', clients=clients)

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
        login_user(user)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/')
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account')
def settings():
    return ""

@app.route('/add-client', methods=["GET", "POST"])
def add_client():
    form = newClient()
    if form.validate_on_submit():
        client = Client()
        client.register(th_id=current_user._id, clnt_name=form.clnt_name.data, gender=form.gender.data, age=form.age.data)
        client.save()
        return redirect(url_for('dashboard'))
    return render_template('add-client.html', form=form)