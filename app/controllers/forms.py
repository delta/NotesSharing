from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    # DataRequired checks if the field is not left empty
    rollnumber = StringField('Roll Number', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    # remember_me = BooleanField('remember me', default = False)



class MetaData(Form):
        author = StringField('Author of notes',validators=[DataRequired()])
        tags  = StringField('Enter tags',validators=[DataRequired()])  
        description = StringField('Enter description', validators =[DataRequired()])

class Search(Form):
        query = StringField('Search whatever you want')

