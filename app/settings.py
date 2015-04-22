import os 
class Config(object):
        SECRET_KEY = 'HAHAHAH-FUCK-YOU'
        basedir = os.path.abspath(os.path.dirname(__file__))
        WTF_CSRF_ENABLED = True
        UPLOAD_FOLDER = basedir + '/../tmp'
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','odp','pptx','docx','doc','ppt','rtf'])
        IMAP_SERVER = 'webmail.nitt.edu'
        IMAP_SERVER_PORT = '143'
        WHOOSH_BASE = os.path.join(basedir, 'search.db') #A special database that is dedicated to full text search

class DevConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.db' + '?check_same_thread=False'


class ProdConfig(Config):
        pass
