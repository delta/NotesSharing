import os 
class Config(object):
        SECRET_KEY = 'HAHAHAH-FUCK-YOU'
        basedir = os.path.abspath(os.path.dirname(__file__))
        WTF_CSRF_ENABLED = True
        UPLOAD_FOLDER = basedir + '/../tmp'
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','odp','pptx','docx'])
        IMAP_SERVER = 'webmail.nitt.edu'
        IMAP_SERVER_PORT = '143'


class DevConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///controllers/app.db'


class ProdConfig(Config):
        pass
