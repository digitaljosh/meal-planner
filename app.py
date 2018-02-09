from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from hidden import local_db_connect

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = local_db_connect

app.secret_key = 'amsdfsndfknasdlfknl'


app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

