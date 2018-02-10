
from flask import Flask, render_template, request, json, request
#from rapidconnect import RapidConnect
import requests
import json

#from flask_sqlalchemy import SQLAlchemy 
import json 
import pprint 

from datetime import date
import calendar

from models import User, Calendar, Recipe
from app import app, db



#GET Search Recipes - spoonacular
@app.route('/search', methods=['POST', 'GET'])
def recipe_search():

    if request.method == 'POST':
        
        search_query = request.form['search']
        search_query = search_query.replace(" ","+")

        api = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&query="
        url = api + search_query
        headers={
            "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
            "Accept": "application/json"
            }

        json_data = requests.get(url, headers=headers).json()

        

        print("########################################")
        print("json_data Type: ")
        print(type(json_data))
        #print(json_data)
        print("########################################")

        
        return render_template('search.html', recipe_list=json_data)

    else:
        
        return render_template('search.html')



# Get Recipe Information - spoonacular API 
@app.route('/instructions', methods=['POST', 'GET'])
def recipe_instructions():
    recipe_id = request.args.get('id')
    api_part1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
    api_part2 = "/information?includeNutrition=false"
    url = api_part1 + recipe_id + api_part2
    headers={
    "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
    "Accept": "application/json"
    }

    json_data = requests.get(url, headers=headers).json()


    print("######################")
    print(type(json_data))
    #print(json_data)
    print("Dish Name: ")
    
    try:
        stop_index = json_data['title'].index('-')
        print("INDEX" + str(stop_index))
        dish_name = json_data['title'][:stop_index]
        print(dish_name)
    except ValueError:
        dish_name = json_data['title']
        print(dish_name + "- not the char used in json_data")

    recipe_name = dish_name
    print("######################")
    print("++++++++++++")
    
    #Might try beautiful soup but didn't want to add to reqs just yet 
    pp = pprint.PrettyPrinter(indent=4)
    #print("Ingredients are: " + pp.pprint(json_data[ 'extendedIngredients']['name']))
    #print(pp.pprint(json_data))
    print("===================")
    ingreds = json_data['extendedIngredients']
    print(pp.pprint(ingreds))
    print(ingreds[4]['originalString'])
    print(len(ingreds))
    print("*******************")
    print("AND the ingredients are: ")
    recipe_ingredients = []
    for i in range(0, len(ingreds)):
        recipe_ingredients.append(ingreds[i]['originalString'])
        print(ingreds[i]['originalString'])

    print("*********************")
    
    print("Instructions ARE: ")
    print(pp.pprint(json_data['instructions']))

    recipe_instructs = json_data['instructions']

    print("*******************")
    print("Time to cook: ")
    print(pp.pprint(json_data['readyInMinutes']))

    recipe_time =  int(json_data['readyInMinutes'])
    #print("Ingredients are: " + pp.pprint(json_data['name']))# ['extendedIngredients']))#['name']))

    # deserialized_data = json.loads(json_data)
    # pp = pprint.PrettyPrinter(indent=4)
    # print("To Python dict: \n")
    # print(deserialized_data)
    # print("Type check: " + type(deserialized_data))
    # print("+++++++++++++\n")
    # print(pp.pprint(ingredients))
    

# AND now instantiate recipe => TODO pickle ingredients, instructions ?
    #new_recipe = Recipe(recipe_name, recipe_ingredients, recipe_instructs, recipe_time, cookbook_id=None)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("Recipe name type: ")
    print(type(recipe_name))
    print("Recipe ingreds type: ")
    print(type(recipe_ingredients))
    print("Recipe instructions type: ")
    print(type(recipe_instructs))
    print("Recipe time type: ")
    print(type(recipe_time))

    #print(recipe_instructs)
    #TODO convert or make time explicit in minutes 
    new_recipe = Recipe(recipe_name, str(recipe_ingredients), recipe_instructs, recipe_time, cookbook_id=None)

    db.session.add(new_recipe)
    db.session.commit()
    
    return render_template('recipe.html', recipe=new_recipe)
    #return render_template('search.html', recipe_instr=json_data) 



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