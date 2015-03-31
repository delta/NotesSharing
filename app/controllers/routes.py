from flask import render_template, flash, redirect, request, session, url_for, g, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from sqlalchemy import or_, and_
from app import app, db  # Your init files
from .forms import LoginForm , MetaData , Search
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


@app.route('/',methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def index():
    #print form
    if request.method == 'GET':
        return render_template('home.html', title='FireNotes', x=list_departments,search_form = Search())
    elif request.method == 'POST':
        print 'this happened '
        search = request.form['query'].split(' ')
        print search
        tags,author,description = search[0],search[1],search[2]
        all_files = files.query.filter(or_(files.tags.like(tags),
                files.author.like(author),files.description.like(description)))
        list_of_files = [(file.filename,file.author,file.tags,file.description,file.downloads,file.stars,file.uploader) for file in all_files.all()]
        return render_template('notes.html', 
                        list_of_files=list_of_files,
                        search_form = Search())

@app.route('/<name>' , methods = ['GET','POST'])
def navigate(name):
    # name is basically the department
    if request.method == 'GET':
        return render_template('semester.html', dept=name, semesters=semesters,search_form = Search())
    elif request.method == 'POST':
        print 'this happened '
        search = request.form['query'].split(' ')
        print search
        tags,author,description = search[0],search[1],search[2]
        all_files = files.query.filter(or_(files.tags.like(tags),
                files.author.like(author),files.description.like(description)))
        list_of_files = [(file.filename,file.author,file.tags,file.description,file.downloads,file.stars,file.uploader) for file in all_files.all()]
        return render_template('notes.html', 
                        list_of_files=list_of_files,
                        search_form = Search())

@app.route('/<name>/<semester>', methods=['GET', 'POST'])
def UploadOrView(name, semester):
    
    form = MetaData() 
    search_form = Search() 
    if request.method == 'GET':
        '''
                Get all the files from the db and display to the user
        '''
        all_files = files.query.filter(and_(files.department.like(name),
                                            files.semester.like(int(semester))))
        list_of_files = [(file.filename,file.author,file.tags,file.description,file.downloads,file.stars,file.uploader) for file in all_files.all()]
        return render_template("notes.html", list_of_files=list_of_files, dept=name, sem=semester,form=form,search_form = Search())

    elif request.method == 'POST':
        if session['rollnumber'] and session['dept'] == name:
            file = request.files['pdf']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploads = files(filename=filename, department=name, semester=semester, author= request.form['author'], tags = request.form['tags'], description = request.form['description'],downloads = 0 , stars = 0, uploader = session['rollnumber'])
            db.session.add(uploads)
            db.session.commit()
            all_files = files.query.filter(and_(files.department.like(name),
                                               files.semester.like(int(semester))))
            list_of_files = [(file.filename,file.author,file.tags,file.description,file.downloads,file.stars,file.uploader) for file in all_files.all()]
            return render_template('notes.html', list_of_files=list_of_files, dept=name, sem=semester,form=form,search_form = Search())
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
    return send_file("../tmp/" + download_file, attachment_filename=download_file, as_attachment=True)


@app.route('/login', methods=['GET', 'POST'])
def login():

    search_form = Search()
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', title='Sign In', form=form,search_form = Search())
    elif request.method == 'POST':
        # Whether all parts of the form is submitted or not
        if form.validate_on_submit():
            form.rollnumber = request.form['rollnumber']
            valid_login = server_login(request.form['rollnumber'], request.form['password'])
            if not valid_login:
                return redirect(url_for('login'))
            else:
                user = User.query.filter_by(rollNo = request.form['rollnumber']).all()
                if not len(user):
                        new_entry = User(rollNo = request.form['rollnumber'])
                        db.session.add(new_entry)
                        db.session.commit()
                return redirect(url_for('navigate', name=session['dept']))
    
    return render_template('login.html', title='Sign In', form=form,search_form = Search())


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))
