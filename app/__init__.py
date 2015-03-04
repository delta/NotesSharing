from flask import Flask 

app = Flask(__name__) #Our Flask instance 
app.config.from_object('config') #Setting our WTF config

from app import views 
