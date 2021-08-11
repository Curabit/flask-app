from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError
from wtforms.fields.html5 import EmailField
from app.models import User

class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Email()])
    psw = PasswordField(validators=[InputRequired()], id='psw')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField(label="Sign In", render_kw={"class": "dark-btn"})

class RegisterForm(FlaskForm):
    th_name = StringField(validators=[InputRequired()])
    clinic_name = StringField(validators=[InputRequired()])
    clinic_add = TextAreaField(validators=[InputRequired()])
    email = EmailField(validators=[InputRequired(), Email()])
    # TODO: Add password validation
    psw = PasswordField(validators=[InputRequired()], id='psw')
    psw2 = PasswordField(validators=[InputRequired(), EqualTo(fieldname='psw', message="Passwords do not match.")], id='psw2')
    agreement = BooleanField(validators=[InputRequired()])
    submit = SubmitField(label="Sign Up", render_kw={"class": "dark-btn"})

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('This email ID is already registered.')