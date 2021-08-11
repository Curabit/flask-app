from flask import render_template, flash, redirect, jsonify, url_for, request
from app import app
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.exceptions import InternalServerError, MethodNotAllowed

@app.route('/')
@login_required
def index():
    return render_template('index.html')

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
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
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
                next_page = url_for('index')
            else:
                return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/500")
def t500():
    raise InternalServerError()

@app.route("/405")
def t405():
    raise MethodNotAllowed()