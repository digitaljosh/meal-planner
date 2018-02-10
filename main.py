from flask import render_template, redirect, request, flash, session
from app import app, db

from datetime import date
import calendar

from models import User, Calendar




@app.route("/")
def index():
    return render_template('splash.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    # loops home for now, doesn't break 
    if request.method == 'GET':
        return render_template('/sign-up.html')
    elif request.method == 'POST':
        
        name = request.form['username']
        email = request.form['email']
        p_word = request.form['passw']
        con_pword = request.form['conf_pass']

        user_with_same_name = User.query.filter_by(username=name).count()

        #TODO test email 
        """
        elif email != valid: #regex test match
            flash("Not a valid email", 'negative')
            return render_template('sign-up.html', username=name)
            """
        if user_with_same_name > 0:
            flash("Someone is already using that name", 'negative')
            return render_template('sign-up.html')
        
        elif p_word != con_pword:
            flash("Passwords don't match!", 'negative')
            return render_template('sign-up.html', username=name, email=email)

        else:
            # everything entered correctly we instantiate 
            new_user = User(name, p_word, email)
            # and commit to database
            db.session.add(new_user)
            db.session.commit()
            # here is where we are going to establish a new calendar for user ? for this month
            # TODO is the calendar object for the year !
            today = date.today()
            print("++++++++++= " + str(today.year))
            print("User id =  " + str(new_user.id))
            #new_user_calendar = Calendar(year=int(today.year), user_ids=new_user.id)
            # new calendar for user for current year(need to think about if set up in December for instance)
            new_user_calendar = Calendar(today.year, new_user.id)
            print("newCal year =  " + str(new_user_calendar.year))
            db.session.add(new_user_calendar)
            db.session.commit()

            session['username'] = new_user.username
            cal = Calendar.query.filter_by(user_ids=new_user.id).first()

            print("%%%%%%%%%%%%%%%%%" + str(cal.year))
            py_cal_html = calendar.HTMLCalendar()
            cal_HTML = py_cal_html.formatyearpage(cal.year)
            return render_template('calendar.html', username=session['username'], cal=cal_HTML)


        

@app.route('/login', methods=['GET', 'POST'])
def login():
    # just loops back home for now since no db
    if request.method == 'GET':
        try:
            if session['username']:
                flash("You're logged in!", 'positive')
                return redirect('/calendar.html', username=session['username'])
        except KeyError:
            return render_template('login.html')
    elif request.method == 'POST':
        tried_name = request.form['username']
        tried_pw = request.form['password']
        user_to_check = User.query.filter_by(username=tried_name)

        if user_to_check.count() == 1:
            user = user_to_check.first()
            if user.password == tried_pw:
                session['username'] = tried_name
                return render_template('calendar.html', username=session['username'])
            else:
                flash("Nice try!", 'negative')
                return redirect('/login')
        else:
            flash("Either you mistyped your username or you don't have an account.", 'negative')
            return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        if session['username']:
            del session['username']
            flash("See ya next time!", 'positive')
            return redirect("/")
    except KeyError:
        flash("You aren't currently logged in!", 'negative')
        return redirect("/")



if __name__ == '__main__':
    app.run()