from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from boto.s3.connection import S3Connection

import os 
#from hidden import heroku_db_connect, shhh


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"
secret_conn = S3Connection(os.environ['S3_Key'], os.environ['S3_SECRET'])
#heroku_db_connect = S3Connection(os.environ['DATABASE_URL'])
#shhh = S3Connection(os.environ['SECRET_KEY'])
heroku_db_connect = secret_conn(['DATABASE_URL'])
shhh = secret_conn(['SECRET_KEY'])

app.config['SQLALCHEMY_DATABASE_URI'] = heroku_db_connect
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = shhh

app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

