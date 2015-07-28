from flask import render_template, flash, redirect, request, session, url_for, g, send_file
from flask.ext.login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from sqlalchemy import or_, and_
from app import app, db ,lm
from .forms import LoginForm , MetaData , Search
from ..models import Department, files,User
import os
from .auth import server_login, DEPARTMENTS
import stars
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import indexer
from celery import Celery

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

fileformat = re.compile(r'(\w*)\.(\w*)')
departments = Department.query.all()
list_departments = []
for dept in departments:
    list_departments.append(dept.department)
semesters = [i for i in range(1, 9)]
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@celery.task
def indexing(filename):
   indexer.index_it(filename)

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



@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def user_loader(user_rollNo):
    return User.query.get(user_rollNo)

@app.route('/faq', methods = ['GET','POST'])
def faq():
    if request.method == 'GET':
        return render_template("faq.html",search_form = Search())
    elif request.method == 'POST':
        if request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))

@app.route('/',methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
@app.route('/home', methods = ['GET','POST'])
def index():
    form = Search()
    if request.method == 'GET':
        return render_template('home.html', title='FireNotes', x=list_departments,search_form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('shownotes',query = form.query.data))


@app.route('/show/<query>',methods = ['GET','POST'])
@app.route('/show/<query>/',methods = ['GET','POST'])
def shownotes(query):
    form = Search()
    if request.method == 'GET':
        has_starred = False
        list_of_files = []
        all_files = []
        list_of_files = []
        uniq = {}
        try:
            books = indexer.search(query)
            for x in books:
                all_files  = files.query.filter(files.filename.like(x))
                for file in all_files:
                    try:
                        if uniq[file.filename]:
                            print "Duplicate"
                    except:
                        list_of_files.append((file.filename,file.author,file.tags,file.semester,file.description,file.downloads, (has_starred, stars.get_stars(file.id), file.id), file.uploader, file.upload_date.strftime("%d-%m-%Y %H:%M"),file.department))
                        uniq[file.filename] = True
                    try:
                        has_starred = stars.has_starred(file.id, g.user.rollNo)
                    except:
                        pass
        except:
            pass
        indexed_search = files.query.whoosh_search(query)
        has_starred = False
        for file in indexed_search:
            try:
                has_starred = stars.has_starred(file.id, g.user.rollNo)
            except:
                pass
            list_of_files.append((file.filename,file.author,file.tags,file.semester,file.description,file.downloads, (has_starred, stars.get_stars(file.id), file.id), file.uploader, file.upload_date.strftime("%d-%m-%Y %H:%M"),file.department))
        return render_template('notes.html',list_of_files = list_of_files , search_form = form)


    elif request.method == 'POST':
        if request.form.get('star'):
            print 'AHAHH'
            print '{0} is the form'.format(request.form)
            if request.form['star'] == '1':
                stars.add_star(request.form['file_id'], request.form['user_rno'])
            if request.form['star'] == '-1':
                stars.reduce_star(request.form['file_id'],request.form['user_rno'])
            return "FUCK YEAH"
        if request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))


@app.route('/<name>/' , methods = ['GET','POST'])
@app.route('/<name>' , methods = ['GET','POST'])
def navigate(name):
    form = Search()
    if request.method == 'GET':
        if name not in DEPARTMENTS.values():
            return redirect(url_for('index'))
        return render_template('semester.html', dept=name, semesters=semesters,search_form = Search())
    elif request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('shownotes',query = form.query.data))


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
                has_starred = stars.has_starred(file.id, g.user.rollNo)
            except:
                pass
            list_of_files.append((file.filename,file.author,file.tags,file.semester,file.description,file.downloads, (has_starred, stars.get_stars(file.id), file.id), file.uploader, file.upload_date.strftime("%d %b %Y %H:%M"),file.department))

        list_of_files = list(set(list_of_files))
        return render_template("notes.html", list_of_files=list_of_files, dept=name, sem=semester,form=form,search_form = Search())

    elif request.method == 'POST':
        if request.form.get('star'):
            if request.form['star'] == '1':
                stars.add_star(request.form['file_id'], request.form['user_rno'])
            if request.form['star'] == '-1':
                stars.reduce_star(request.form['file_id'],request.form['user_rno'])
            return "FUCK YEAH"
        if request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))


@app.route('/<name>/<semester>/<filename>')
def Download(name , semester, filename):
    checkoutformat = re.search(fileformat,filename)
    if checkoutformat.group(2) in ['jpg','jpeg','png','bmp']:
        # surely there will be a pdf
        download_file = checkoutformat.group(1)+'.pdf'
        #updated_file = files.query.filter_by(filename = filename).first()
        if name is not None and semester is not None:
            updated_file = files.query.filter(and_(files.department.like(name),
                                               files.semester.like(int(semester)),
                                               files.filename.like(filename))).scalar()
        else:
            updated_file = files.query.filter(files.filename.like(filename)).scalar()
        updated_file.downloads += 1
        db.session.commit()
        return send_file("../tmp/" + download_file, attachment_filename=download_file, as_attachment=True)
    else:
        download_file = filename
        if name is not None and semester is not None:
            updated_file = files.query.filter(and_(files.department.like(name),
                                               files.semester.like(int(semester)),
                                               files.filename.like(filename))).scalar()
        else:
            updated_file = files.query.filter(files.filename.like(filename)).scalar()
        updated_file.downloads += 1
        db.session.commit()
        return send_file("../tmp/" + download_file, attachment_filename=download_file, as_attachment=True)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    search_form = Search()
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', title='Sign In', form=form,search_form = Search())
    elif request.method == 'POST':
        if form.validate_on_submit():
            valid_login = server_login(form.rollnumber.data, form.password.data)
            if not valid_login[0]:
                return redirect(url_for('login'))
            else:
                print form.rollnumber.data
                user = User.query.get(form.rollnumber.data)
                if user is None:
                    new_entry = User(rollNo = form.rollnumber.data)
                    new_entry.year , new_entry.dept = valid_login[1],valid_login[2]
                    new_entry.authenticated=True
                    db.session.add(new_entry)
                    db.session.commit()
                    login_user(new_entry)
                    return redirect(url_for('navigate',name=g.user.dept))
                user.authenticated = True
                login_user(user)
                return redirect(url_for('navigate', name=g.user.dept))

        if request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index'))


@app.route('/<name>/<semester>/upload', methods=['GET', 'POST'])
def Upload(name, semester):

    form = MetaData()
    search_form = Search()
    if request.method == 'GET':
       return render_template("upload.html",dept=name, sem=semester,form=form,search_form = Search())

    elif request.method == 'POST':
        if request.form.get('query'):
            query = request.form['query']
            return redirect(url_for('shownotes',query = query))

        if g.user.rollNo and g.user.dept==name:
            uploaded_files = request.files.getlist('pdf')
            picture_files = []

            for file in uploaded_files:
                fileFormat =  file.content_type
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    checkformat = re.search(fileformat,filename)
                    if checkformat:
                        if checkformat.group(2) in ['png','jpg','jpeg','bmp','gif']:
                            picture_files.append(filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if len(picture_files) == 0:
                    print ' this shouldnt happen'
                    uploads = files(filename=filename, department=name, semester=semester, author= request.form['author'], tags = request.form['tags'], description = request.form['description'],downloads = 0, uploader = g.user.rollNo, upload_date = datetime.datetime.now())
                    db.session.add(uploads)
                    db.session.commit()

                    #indexing.apply_async((filename,))
                    #indexer.index_it(filename, fileFormat)

            if picture_files:
                picture_files =  [app.config['UPLOAD_FOLDER']+'/'+f  for f in picture_files]
                c = canvas.Canvas(app.config['UPLOAD_FOLDER'] + '/' + checkformat.group(1)+'.pdf',pagesize=(460.0,820.0))
                width , height = (460.0,820.0)
                for pics in picture_files:
                    c.drawImage(pics,0,0)
                    c.showPage()
                    c.save()
                uploads = files(filename=filename,department=name, semester=semester, author= request.form['author'], tags = request.form['tags'], description = request.form['description'],downloads = 0, uploader = g.user.rollNo, upload_date = datetime.datetime.now())
                db.session.add(uploads)
                db.session.commit()

            all_files = files.query.filter(and_(files.department.like(name),
                                               files.semester.like(int(semester))))
            has_starred = False
            list_of_files = []
            for file in all_files.all():
                try:
                    has_starred = stars.has_starred(file.id, g.user.rollNo)
                except:
                    pass
                list_of_files.append((file.filename,file.author,file.tags,file.semester,file.description,file.downloads, (has_starred, stars.get_stars(file.id), file.id), file.uploader, file.upload_date.strftime("%d-%m-%Y %H:%M"),file.department))
            return redirect(url_for('UploadOrView',name=name, semester=semester) )
        else:
            return redirect(url_for('navigate'))

