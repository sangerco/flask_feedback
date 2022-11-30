from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email

class UserForm(FlaskForm):
    """ form to register new user """

    username = StringField("Username", validators=[InputRequired(), "Please enter a valid username"])
    password = PasswordField("Password", validators=[InputRequired(), "Please enter a valid password"])
    email = StringField("Email Address", validators=[Email(), "Please enter a valid email address"])
    first_name = StringField("First Name", validators=[InputRequired(), "Field cannot be left blank!"])
    last_name = StringField("Last Name", validators=[InputRequired(), "Field cannot be left blank!"])

class LoginForm(FlaskForm):
    """ form to login existing user """

    username = StringField("Username", validators=[InputRequired(), "Please enter a valid username"])
    password = PasswordField("Password", validators=[InputRequired(), "Please enter a valid password"])