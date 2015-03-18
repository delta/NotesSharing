import flask
from flask.ext.sqlalchemy import SQLAlchemy
# We also need to initialize our database


app = flask.Flask(__name__)  # Our Flask instance
app.config.from_object('config')  # Setting our WTF config
db = SQLAlchemy(app)

from controllers import routes
import models
