from flask import render_template, flash, redirect, request, session, url_for, g, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from sqlalchemy import or_, and_
from app import app, db  # Your init files
from .forms import LoginForm
from ..models import Department, files,User
import os
from .auth import server_login

departments = Department.query.all()
list_departments = []
for dept in departments:
    list_departments.append(dept.department)
semesters = [i for i in range(1, 9)]


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    print list_departments
    return render_template('home.html', title='FireNotes', x=list_departments)


@app.route('/<name>')
def navigate(name):
    # name is basically the department
    return render_template('semester.html', dept=name, semesters=semesters)


@app.route('/<name>/<semester>', methods=['GET', 'POST'])
def UploadOrView(name, semester):

    if request.method == 'GET':
        '''
                Get all the files from the db and display to the user
        '''
        all_files = files.query.filter(and_(files.department.like(name),
                                            files.semester.like(int(semester))))
        list_of_files = [(file.id, file.filename) for file in all_files.all()]
        return render_template("notes.html", list_of_files=list_of_files, dept=name, sem=semester)

    elif request.method == 'POST':
        if session['rollnumber'] and session['dept'] == name:
            file = request.files['pdf']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print ' okay we are uploading the file '
            uploads = files(filename=filename, department=name, semester=semester)
            db.session.add(uploads)
            db.session.commit()
            all_files = files.query.filter(or_(files.department.like(name),
                                               files.semester.like(int(semester))))
            list_of_files = [(file.id, file.filename) for file in all_files.all()]
            return render_template('notes.html', list_of_files=list_of_files, dept=name, sem=semester)
        else:
            return redirect(url_for('navigate'))


@app.route('/static/css/<filename>')
def serveCss(filename):
    return send_file("static/css/"+filename)

@app.route('/static/fonts/<filename>')
def serveFonts(filename):
    return send_file("static/fonts/"+filename)

@app.route('/static/js/<filename>')
def serveJs(filename):
    return send_file("static/js/"+filename)

@app.route('/static/images/<filename>')
def serveImages(filename):
    return send_file("static/images/"+filename)

@app.route('/<name>/<semester>/<filename>')
def Download(name, semester, filename):
    download_file = filename
    print 'Oh yeah we are gonna download the file'
    return send_file("../tmp/" + download_file, attachment_filename=download_file, as_attachment=True)


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', title='Sign In', form=form)

    elif request.method == 'POST':
        # Whether all parts of the form is submitted or not
        if form.validate_on_submit():
            flash('Login requested for Department = {0}'.format(form.rollnumber))
            form.rollnumber = request.form['rollnumber']
            print request.form['rollnumber']
            #  print request.form['password']
            valid_login = server_login(request.form['rollnumber'], request.form['password'])
            print valid_login
            if not valid_login:
                print 'fuck'
                return redirect(url_for('login'))
            else:
                # check if the rollnumber exist in the user database 
                # if it doesnt then add it to the db 
                # else redirect to index 
                user = User.query.filter_by(rollNo = request.form['rollnumber']).all()
                if not len(user):
                        new_entry = User(rollNo = request.form['rollnumber'])
                        db.session.add(new_entry)
                        db.session.commit()
                        print 'new Entry added baby'
                print 'Logged in'
                return redirect(url_for('navigate', name=session['dept']))
    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))
