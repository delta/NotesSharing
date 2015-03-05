from flask import render_template , flash , redirect,request 
from app import app,models,db
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
        return 'Welcome to Fire Notes'


@app.route('/login',methods = ['GET','POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit(): #Whether all parts of the form is submitted or not
                flash('Login requested for Department = {0}'.format(form.department))
                departments = models.Department.query.all()
                list_departments  = []
                for dept in departments :
                        list_departments.append(dept.department)
                
                form.department = request.form['department']
                if form.department in list_departments:
                        print 'yes'
                        return redirect('/')
                else :
                        print 'fuck'
                        return render_template('login.html',title='Sign In', form=form)

        return render_template('login.html',title='Sign In', form=form)



