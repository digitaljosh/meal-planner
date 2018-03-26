from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from hidden import jason_db_connect, josh_db_connect, aws_db_connect

application = Flask(__name__)

#application.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"

# Comment out other devs' db's to run the application locally
#application.config['SQLALCHEMY_DATABASE_URI'] = jason_db_connect
#application.config['SQLALCHEMY_DATABASE_URI'] = josh_db_connect
application.config['SQLALCHEMY_DATABASE_URI'] = aws_db_connect

application.secret_key = 'Shhhhh,dont_tell_anyone1979'

application.config['SQLALCHEMY_ECHO'] = True
application.config['DEBUG'] = True

db = SQLAlchemy(application)

