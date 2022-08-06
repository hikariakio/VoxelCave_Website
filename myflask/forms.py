from flask_wtf import FlaskForm
import re
from wtforms.fields import SubmitField, StringField,EmailField,TelField
from wtforms.validators import InputRequired, Email,Regexp  ,Length

# form used in basket
class CheckoutForm(FlaskForm):
    firstname = StringField("First Name", validators=[InputRequired(message="Enter your first name.")])
    lastname = StringField("Last Name", validators=[InputRequired(message="Enter your last name.")])
    email = StringField("Email Address", validators=[InputRequired("Enter your email address."), Email("Please enter a valid email.")])
    phone = TelField("Phone Number", validators=[InputRequired(message='Enter your phone number.'),Regexp(regex='^[+-]?[0-9]+',flags = 0,message = 'Please enter a vaild phone number.')])
    submit = SubmitField("Confirm") 