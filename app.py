from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ
from dotenv import load_dotenv



app = Flask(__name__)


dotenv_path = path.join(path.dirname(__file__), 'eat.env')
load_dotenv(dotenv_path)

#environ.update(dotenv)

#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"

# Comment out other devs' db's to run the app locally
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("jason_db_connect")
#app.config['SQLALCHEMY_DATABASE_URI'] = josh_db_connect

#pulled this from environ here rather than main to limit imports
mash_key = environ.get("mash_key")

app.secret_key = environ.get("shhh")

app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app)

