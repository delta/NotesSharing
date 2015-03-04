from flask import render_template , flash , redirect 
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
        return 'Hello world'


@app.route('/login',methods = ['GET','POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit(): #Whether all parts of the form is submitted or not
                flash('Login requested for Department = {0}'.format(form.department))
                return redirect('/')

        return render_template('login.html',title='Sign In', form=form)



