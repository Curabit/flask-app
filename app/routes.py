from app.mails import ackSignUp, notifySignUp, resetPass
from app import app
from flask import url_for, redirect, render_template, flash, request
from werkzeug.urls import url_parse
from app.forms import formForgotPassword, formLogin, formRegisterTherapist, formResetPassword
from app.models import User
from flask_login import current_user, login_user

# @app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == 'therapist':
            return redirect(url_for('th_dashboard'))
        elif current_user.user_type == 'admin':
            return redirect(url_for('admin_dashboard'))
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
            resetPass(email=user.email, th_name=user.name, token=user.get_reset_password_token())
            flash('An email has been sent to you with instructions on how to reset your password.')
            return redirect(url_for('login'))
    return render_template('forgot_psw.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('login'))
    form = formResetPassword()
    if form.validate_on_submit():
        user.set_hash(form.new_psw.data)
        user.save()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_psw.html', form=form)