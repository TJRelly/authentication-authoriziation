from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    """Form to register users."""
    
    email = EmailField('Email', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])  
    
class LoginForm(FlaskForm):
    """Form to register users."""
    
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    
class EditFeedbackForm(FlaskForm):
     """Form to edit feedback"""
     title = StringField('Title', validators=[DataRequired(), Length(max=100)])
     comment = StringField('Comment', validators=[DataRequired()])
     
       