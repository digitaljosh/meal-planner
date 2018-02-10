from flask import render_template, redirect, request, session, json, flash
import requests
import json
import recipe_search_list, recipe_info


#from flask_sqlalchemy import SQLAlchemy 

from datetime import date
import calendar

from app import app, db
from models import User, Calendar
from hashy import check_pw_hash




#GET Search Recipes - spoonacular
@app.route('/search', methods=['POST', 'GET'])
def recipe_search():

    if request.method == 'POST':
        '''
        -The following code block calls spoonacular api, using temp data during development-

        search_query = request.form['search']
        search_query = search_query.replace(" ","+")
        api = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&query="
        url = api + search_query
        headers={
            "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
            "Accept": "application/json"
            }

        json_data = requests.get(url, headers=headers).json()

        print("##############")
        print(recipe_temp)
        print("################")
        return render_template('search.html', recipe_list=json_data)
        '''
        recipe_list = recipe_search_list.recipe_search_list #call r_s_l variable within r_s_l module
        return render_template('search.html', recipe_list=recipe_list )

    else:
        
        return render_template('search.html')



# Get Recipe Information - spoonacular API 
@app.route('/instructions', methods=['POST', 'GET'])
def recipe_instructions():

    '''
    -The following code block calls spoonacular api, using temp data during development-

    recipe_id = request.args.get('id')
    api_part1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
    api_part2 = "/information?includeNutrition=false"
    url = api_part1 + recipe_id + api_part2
    headers={
    "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
    "Accept": "application/json"
    }

    json_data = requests.get(url, headers=headers).json()

    return render_template('search.html', recipe_instr=json_data) 
    '''

    recipe_instructions = recipe_info.recipe_info # call recipe_info variable within recipe_info module
    return render_template('search.html', recipe_instructions=recipe_instructions )


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
            if user and check_pw_hash(tried_pw, user.pw_hash):
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