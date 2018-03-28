from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from hidden import heroku_db_connect

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"


app.config['SQLALCHEMY_DATABASE_URI'] = heroku_db_connect

app.secret_key = 'Shhhhh,dont_tell_anyone1979'

app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

