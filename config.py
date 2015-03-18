import os 

WTF_CSRF_ENABLED = True
SECRET_KEY = 'HAHAHA-FUCK-YOU'
basedir = os.path.abspath(os.path.dirname(__file__))

# For migration purpose 
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

print basedir 


#Where we are going to store the files 
UPLOAD_FOLDER = basedir+'/tmp/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# IMAP Login Config
IMAP_SERVER_IP = ''
IMAP_SERVER_PORT = ''