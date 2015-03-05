import os 

WTF_CSRF_ENABLED = True
SECRET_KEY = 'HAHAHA-FUCK-YOU'
basedir = os.path.abspath(os.path.dirname(__file__))

# For migration purpose 
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

