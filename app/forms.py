from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_login import current_user

#LOGIN FORM
class LoginForm(FlaskForm):
    """
    Initializing the login fields
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")

# REGISTER FORM
class RegisterForm(FlaskForm):
    """
    Initializing the register fields
    """
    fullname = StringField("Fullname", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_no = IntegerField("Phone No", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email")
        
    def validate_phone(self, phone_no):
        user = User.query.filter_by(phone_no=phone_no.data).first()
        if user is not None:
            raise ValidationError("Please use a different phone number")
               
# ADMIN FORM
class AdminForm(FlaskForm):

    id_no = IntegerField("ID number", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Sign In")

# ENTRY FORM 
class Entry(FlaskForm):
    phone_no = IntegerField("phone_no", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    points = IntegerField("points", validators=[DataRequired()])
    pin = PasswordField("pin", validators=[DataRequired()])
    submit = SubmitField("Send")


#RESET FORM

class ResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

#RESET_PASSWORD FORM

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    repeat_password = PasswordField("repeat password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset password")