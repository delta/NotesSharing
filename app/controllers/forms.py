from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    # DataRequired checks if the field is not left empty
    rollnumber = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    # If you have validators attached , they have errors added under form.fieldname.erros
    # remember_me = BooleanField('remember me', default = False)
