from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 

#TODO break main apart into seperate files later
app = Flask(__name__)

app.config['SQALCHEMY_DATABASE_URI'] = 'setup localhost phpmyadmin here'
db = SQLAlchemy(app)


app.config['SQLALCHEMY_ECHO'] = True 
app.config['DEBUG'] = True



@app.route("/")
def index():

    return render_template('splash.html')

@app.route('/login')
def login():
    return render_template('/login.html')

@app.route('/sign-up')
def signup():
    return render_template('/sign-up.html')

if __name__ == '__main__':
    app.run()