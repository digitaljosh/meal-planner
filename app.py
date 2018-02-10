from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from hidden import local_db_connect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DinDin:1meal@localhost:3306/DinDin'

app.secret_key = 'amsdfsndfknasdlfknl'

app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

