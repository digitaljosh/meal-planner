from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from hidden import jason_db_connect, josh_db_connect

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"

# Comment out other devs' db's to run the app locally
# app.config['SQLALCHEMY_DATABASE_URI'] = jason_db_connect
app.config['SQLALCHEMY_DATABASE_URI'] = josh_db_connect


app.secret_key = 'Shhhhh,dont_tell_anyone1979'

app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

