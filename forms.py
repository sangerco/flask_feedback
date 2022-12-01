from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class UserForm(FlaskForm):
    """ form to register new user """

    username = StringField("Username", validators=[InputRequired(message="Please enter a valid username")])
    password = PasswordField("Password", validators=[InputRequired(message= "Please enter a valid password")])
    email = StringField("Email Address", validators=[Email(message="Please enter a valid email address"), InputRequired(message="Please enter a valid email address")])
    first_name = StringField("First Name", validators=[InputRequired(message="Field cannot be left blank!")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Field cannot be left blank!")])

class LoginForm(FlaskForm):
    """ form to login existing user """

    username = StringField("Username", validators=[InputRequired(message="Please enter a valid username")])
    password = PasswordField("Password", validators=[InputRequired(message="Please enter a valid password")])

class FeedbackForm(FlaskForm):
    """ feedback form """

    title = StringField("Title", validators=[Length(max=100, message="Title must be less than 100 characters.")])
    content = StringField("Content")