from flask import Flask, render_template, redirect, request 
#from flask_sqlalchemy import SQLAlchemy 

#TODO break main apart into seperate files later
app = Flask(__name__)

#app.config['SQALCHEMY_DATABASE_URI'] = 'setup localhost phpmyadmin here'
#db = SQLAlchemy(app)


#app.config['SQLALCHEMY_ECHO'] = True 
app.config['DEBUG'] = True



@app.route("/")
def index():
    return render_template('splash.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # just loops back home for now since no db
    if request.method == 'GET':
        return render_template('/login.html')
    elif request.method == 'POST':
        return redirect("/")

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    # loops home for now, doesn't break 
    if request.method == 'GET':
        return render_template('/sign-up.html')
    elif request.method == 'POST':
        return redirect("/")

if __name__ == '__main__':
    app.run()