from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField
from app.models import User
from flask_login import current_user

class formLogin(FlaskForm):
    email = EmailField(validators=[InputRequired(), Email()])
    psw = PasswordField(validators=[InputRequired()], id='psw')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField(label="Log In", render_kw={"class": "dark-btn", "style": "width: 50%;"})

class formForgotPassword(FlaskForm):
    email = EmailField(validators=[InputRequired(), Email()])
    submit = SubmitField(label="Send Password Reset Instructions", render_kw={"class": "dark-btn", "style": "width: 50%;"})

class formRegisterTherapist(FlaskForm):
    th_name = StringField(validators=[InputRequired()])
    clinic_name = StringField(validators=[InputRequired()])
    clinic_add = TextAreaField(validators=[InputRequired()])
    email = EmailField(validators=[InputRequired(), Email()])
    psw = PasswordField(validators=[InputRequired()], id='psw')
    psw2 = PasswordField(validators=[InputRequired(), EqualTo(fieldname='psw', message="Passwords do not match.")], id='psw2')
    agreement = BooleanField(validators=[InputRequired("You cannot sign up unless you accept.")])
    submit = SubmitField(label="Register", render_kw={"class": "dark-btn", "style": "width: 50%;"})

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('This email ID has been already registered.')

class formEditTherapist(FlaskForm):
    th_name = StringField(validators=[InputRequired()])
    clinic_name = StringField(validators=[InputRequired()])
    clinic_add = TextAreaField(validators=[InputRequired()])
    email = EmailField(validators=[InputRequired(), Email()])
    submit = SubmitField(label="Save", render_kw={"class": "btn dark-btn"})

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None and user.email != current_user.email:
            raise ValidationError('This email ID is already registered.')

class formChangePassword(FlaskForm):
    curr_psw = PasswordField(validators=[InputRequired()], id='curr_psw')
    new_psw = PasswordField(validators=[InputRequired()], id='new_psw')
    new_psw2 = PasswordField(validators=[InputRequired(), EqualTo(fieldname='new_psw', message="Passwords do not match.")], id='new_psw2')
    submit = SubmitField(label="Change Password", render_kw={"class": "btn dark-btn"})

class formResetPassword(FlaskForm):
    new_psw = PasswordField(validators=[InputRequired()], id='new_psw')
    new_psw2 = PasswordField(validators=[InputRequired(), EqualTo(fieldname='new_psw', message="Passwords do not match.")], id='new_psw2')
    submit = SubmitField(label="Create New Password", render_kw={"class": "dark-btn", "style": "width: 50%;"})

class formClient(FlaskForm):
    cl_name = StringField(validators=[InputRequired()])
    gender = SelectField(choices=[('Male','Male'),('Female','Female'),("None", 'Do not wish to disclose')], validators=[InputRequired()])
    age = IntegerField(validators=[InputRequired()])
    submit = SubmitField(label="Add Client", render_kw={"class": "btn dark-btn"})