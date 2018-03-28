from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from hidden import heroku_db_connect

application = Flask(__name__)

#application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"


application.config['SQLALCHEMY_DATABASE_URI'] = heroku_db_connect

application.secret_key = 'Shhhhh,dont_tell_anyone1979'

application.config['SQLALCHEMY_ECHO'] = True
application.config['DEBUG'] = True

db = SQLAlchemy(application)

