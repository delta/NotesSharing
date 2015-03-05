from flask import Flask 
# We also need to initialize our database 
from flask.ext.sqlalchemy import SQLAlchemy 


app = Flask(__name__) #Our Flask instance 
app.config.from_object('config') #Setting our WTF config
db = SQLAlchemy(app)

from app import views ,models
