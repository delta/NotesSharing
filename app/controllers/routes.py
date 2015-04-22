from flask import render_template, flash, redirect, request, session, url_for, g, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from sqlalchemy import or_, and_
from app import app, db  # Your init files
from .forms import LoginForm , MetaData , Search
from ..models import Department, files,User
import os
from .auth import server_login
import stars
import json 

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
        if request.form.get('star'):
            print 'AHAHHA'
            stars.add_star(request.form['file_id'], request.form['user_rno'])
            return 'Status Success'
        
        elif request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))

@app.route('/show/<query>',methods = ['GET','POST'])
@app.route('/show/<query>/',methods = ['GET','POST'])
def shownotes(query):
    if request.method == 'GET':
        indexed_search = files.query.whoosh_search(query)
        has_starred = False
        list_of_files = []
        for file in indexed_search:
            try:
                has_starred = stars.has_starred(file.id, session['rollnumber'])
            except:
                pass
            list_of_files.append((file.filename,file.author,file.tags,file.description,file.downloads, (has_starred, stars.get_stars(file.id), file.id), file.uploader))
        return render_template('notes.html',list_of_files = list_of_files , search_form = Search())
    
    
    elif request.method == 'POST':
        if request.form.get('star'):
            print 'AHAHHA'
            stars.add_star(request.form['file_id'], request.form['user_rno'])
            return 'Status Success'
        if request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))


@app.route('/<name>/' , methods = ['GET','POST'])
@app.route('/<name>' , methods = ['GET','POST'])
def navigate(name):
    # name is basically the department
    if request.method == 'GET':
        return render_template('semester.html', dept=name, semesters=semesters,search_form = Search())
    elif request.method == 'POST':
        if request.form.get('star'):  # Adding star
            stars.add_star(request.form['file_id'], request.form['user_rno'])
            return "Status Success"
        elif request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))


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
        has_starred = False
        list_of_files = []
        for file in all_files.all():
            try:
                has_starred = stars.has_starred(file.id, session['rollnumber'])
            except:
                pass
            list_of_files.append((file.filename,file.author,file.tags,file.description,file.downloads, (has_starred, stars.get_stars(file.id), file.id), file.uploader))
        return render_template("notes.html", list_of_files=list_of_files, dept=name, sem=semester,form=form,search_form = Search())

    elif request.method == 'POST':
        if request.form.get('star'):  # Adding star
            print "LALALAL\n\n\n\n\n"
            stars.add_star(request.form['file_id'], request.form['user_rno'])
            return "1111"
        if request.form.get('query'):  
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))

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
    updated_file = files.query.filter_by(filename = filename).first()
    updated_file.downloads += 1
    db.session.commit()
    return send_file("../tmp/" + download_file, attachment_filename=download_file, as_attachment=True)


@app.route('/filename/<filename>')
def fastdownload(filename):
    updated_file = files.query.filter_by(filename = filename).first()
    updated_file.downloads += 1
    db.session.commit()
    return send_file("../tmp/" + filename, attachment_filename=filename, as_attachment=True)


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
    
        if request.form.get('query'):  
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))
    return render_template('login.html', title='Sign In', form=form,search_form = Search())


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/<name>/<semester>/upload', methods=['GET', 'POST'])
def Upload(name, semester):
    
    form = MetaData() 
    search_form = Search() 
    if request.method == 'GET':
       return render_template("upload.html",dept=name, sem=semester,form=form,search_form = Search())

    elif request.method == 'POST':
        print request.form
        if request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))

        if session['rollnumber'] and session['dept'] == name:
            uploaded_files = request.files.getlist('pdf')
            print uploaded_files
            for file in uploaded_files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    uploads = files(filename=filename, department=name, semester=semester, author= request.form['author'], tags = request.form['tags'], description = request.form['description'],downloads = 0, uploader = session['rollnumber'])
                    db.session.add(uploads)
                    db.session.commit()
            all_files = files.query.filter(and_(files.department.like(name),
                                               files.semester.like(int(semester))))
            has_starred = False
            list_of_files = []
            for file in all_files.all():
                try:
                    has_starred = stars.has_starred(file.id, session['rollnumber'])
                except:
                    pass
                list_of_files.append((file.filename,file.author,file.tags,file.description,file.downloads, (has_starred, stars.get_stars(file.id), file.id), file.uploader))
            return redirect(url_for('UploadOrView',name=name, semester=semester) )
        else:
            return redirect(url_for('navigate'))

