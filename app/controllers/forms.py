from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    # DataRequired checks if the field is not left empty
    rollnumber = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    # remember_me = BooleanField('remember me', default = False)
