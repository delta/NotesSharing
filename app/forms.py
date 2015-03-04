from flask.ext.wtf import Form
from wtforms import StringField , BooleanField 
from wtforms.validators import DataRequired 


class LoginForm(Form):
        department = StringField('Department',validators = [DataRequired()]) #DataRequired checks if the field is not left empty
        # If you have validators attached , they have errors added under form.fieldname.erros
        # remember_me = BooleanField('remember me', default = False)



