from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from boto.s3.connection import S3Connection

import os 


app = Flask(__name__)


# imports config vars from os (Heroku)
shhh = os.environ.get('SECRET_KEY')

heroku_db_connect = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = heroku_db_connect
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = shhh

app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

