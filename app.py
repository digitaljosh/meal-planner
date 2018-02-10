from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DinDin:1meal@localhost:3306/DinDin'
app.secret_key = 'Shhhhh,dont_tell_anyone1979'

app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

