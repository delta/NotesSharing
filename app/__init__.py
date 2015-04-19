import flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
# We also need to initialize our database


app = flask.Flask(__name__)  # Our Flask instance
db = SQLAlchemy(app)

env = os.environ.get('FIRENOTES_ENV','dev')
app.config.from_object('app.settings.%sConfig' % env.capitalize())
app.config['ENV'] = env

# We are setting our environment to development
import flask.ext.whooshalchemy as whooshalchemy
from controllers import routes
import models

whooshalchemy.whoosh_index(app, models.files)
