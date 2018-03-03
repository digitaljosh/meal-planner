
from flask import render_template, redirect, request,json, session, jsonify, flash
import requests
import json
import pprint 
import datetime
#from datetime import date, timedelta, datetime
import calendar
import re 
import sqlalchemy
#from sqlalchemy import IntegrityError

import recipe_search_list, recipe_info
from app import app, db
from models import User, Event, Recipe, Cookbook
from hashy import check_pw_hash

from data_functs import (clean_ingreds, getUserByName, getUsersEvents, write_events, 
                        make_users_events_current, get_meals_for_the_week, get_today_string,
                        get_week_from_string, get_nouns, getListUserRecipes)



#calendar demo copied with adjusts from https://gist.github.com/Nikola-K/37e134c741127380f5d6 
#all_user = User.query.all()

'''
might make another column for user; public(bool)

'''

@app.before_request
def login_required():
    not_allowed_routes = ['cal_display',]
    if request.endpoint in not_allowed_routes and 'username' not in session:
        flash("You need to be logged in to see your calendar!", 'negative')
        return redirect('/')

@app.route('/data')
def return_data():
    ''' Just displays the json events scheduled on calendar '''
    with open("events.json", "r") as input_data:
        # you should use something else here than just plaintext
        # check out jsonfiy method or the built in json module
        # http://flask.pocoo.org/docs/0.10/api/#module-flask.json
        return input_data.read()


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
            # now create a cookbook for that user
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$" + str(new_user.id))
            new_cookbook = Cookbook(owner_id=new_user.id)
            db.session.add(new_cookbook)
            db.session.commit()
            # set current session
            session['username'] = new_user.username
            session['cookbook-id'] = new_cookbook.id
            #since new user no events yet
            #TODO this is where we may add a dinner buddy's events by name or id
            events = []
            write_events(events)
            return render_template('full-calendar.html', user= getUserByName(session['username']), events=events)


        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            if session['username']:
                recipes = Recipe.query.all()
                name = session['username']
                flash("You're logged in!", 'positive')
                return render_template('full-calendar.html', user=getUserByName(name), events=getUsersEvents(name))#, other_users=all_users)#, remove=True)
                return render_template('full-calendar.html', user=getUserByName(name), events=getUsersEvents(name), recipes=recipes)#username=session['username'])
        except KeyError:
            return render_template('login.html')
        except AttributeError: # no one in db yet NoneType
            flash("This is your first rodeo", 'negative')
            return render_template('sign-up.html')
    elif request.method == 'POST':
        tried_name = request.form['username']
        tried_pw = request.form['password']
        user_to_check = User.query.filter_by(username=tried_name)

        if user_to_check.count() == 1:
            user = user_to_check.first()
            if user and check_pw_hash(tried_pw, user.pw_hash):
                session['username'] = user.username
                evs = getUsersEvents(tried_name)
                #new function see data_functs rewrites events.json
                write_events(evs)
                return redirect('/full-calendar')#, user=getUserByName(session['username']), events=getUsersEvents(session['username']))
            else:
                flash("Nice try!", 'negative')
                return redirect('/login')
        else:
            flash("Either you mistyped your username or you don't have an account.", 'negative')
            return render_template('login.html')

@app.route('/full-calendar', methods=['POST', 'GET'])
def cal_display():
    ''' Displays calendar as populated by user's events'''
    user = getUserByName(session['username'])
   
    if request.method == 'GET':
        # simply displays events in current state
        events = getUsersEvents(user.username)
        # strips events of those that have passed
        current_events = make_users_events_current(user.username)
        write_events(current_events)
        recipes = Recipe.query.all()
        return render_template('full-calendar.html', user=user, events=getUsersEvents(user.username), recipes=recipes)
    else: # 'POST'
        # displays calendar with updated changes
        recipes = Recipe.query.all()
        date = request.form['date']
        dinner = request.form['meal']
        print("#"*10 + "DATE & DINNER" + "#"*10)
        print(date)
        print(dinner)
        print("#"*10)
        recipe = Recipe.query.filter_by(name=dinner).first()
        
        #TODO can't add event until Recipe created
        try:
            new_event = Event(meal=recipe.name, date=date, user_id=user.id)
            db.session.add(new_event)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("You don't have a recipe for that yet", 'negative')
            return render_template('full-calendar.html', user=user, recipes=recipes)
        except AttributeError:
            flash("NO dinner date created. Enter both a date and a meal.", 'negative')
            return render_template('full-calendar.html', user=user, recipes=recipes)

        # retrieve the events from updated db
        make_users_events_current(user.username) # keeps users from adding events to the past
        event_list = Event.query.filter_by(user_id=user.id).all()
        write_events(event_list)
        return render_template('full-calendar.html', events=event_list, user=user, recipes=recipes)


#GET Search Recipes - spoonacular
@app.route('/search', methods=['POST', 'GET'])
def recipe_search():

    if request.method == 'POST':
        '''
        -The following code block calls spoonacular api, using temp data during development-
    '''   
        search_query = request.form['search']
        search_query = search_query.replace(" ","+")
        api = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&query="
        url = api + search_query
        headers={
            "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
            "Accept": "application/json"
            }

        json_data = requests.get(url, headers=headers).json()

        # make sure Jinja doesn't break if no recipe 
        if json_data['totalResults'] == 0:
            flash("No recipe listed, maybe check spelling and try again.", 'negative')
            return render_template('search.html')
        else:
            return render_template('search.html', recipe_list=json_data)
        
        
        return render_template('search.html', recipe_list=json_data)
        """
        recipe_list = recipe_search_list.recipe_search_list #call r_s_l variable within r_s_l module
        return render_template('search.html', recipe_list=recipe_list )
        """
    else: # method = GET
        return render_template('search.html')


# Get Recipe Information - spoonacular API 
@app.route('/instructions', methods=['POST', 'GET'])
def recipe_instructions():

    '''
    -The following code block calls spoonacular api, using temp data during development-
    '''
    recipe_id = request.args.get('id')
    api_part1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
    api_part2 = "/information?includeNutrition=false"
    url = api_part1 + recipe_id + api_part2
    headers={
    "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
    "Accept": "application/json"
    }

    json_data = requests.get(url, headers=headers).json()

    try:
        stop_index = json_data['title'].index('-')
        print("INDEX" + str(stop_index))
        dish_name = json_data['title'][:stop_index]
        print(dish_name)
    except ValueError:
        dish_name = json_data['title']
        print(dish_name + "- not the char used in json_data")

    ingreds = json_data['extendedIngredients']
   
    recipe_name = dish_name
    recipe_ingredients = []
    for i in range(0, len(ingreds)):
        recipe_ingredients.append(ingreds[i]['originalString'])
        print(ingreds[i]['originalString'])


    recipe_instructs = json_data['instructions']

    recipe_time =  int(json_data['readyInMinutes'])
   
    # Assumption here, FOR NOW, is that there won't be multiple recipes with the same name and exact same
    same_recipe = Recipe.query.filter_by(name=recipe_name, instructions=recipe_instructs).first()
   
    if same_recipe:
        #already in db, just display that one
        # flash("Already have that one on file.", 'positive')
        return render_template('recipe.html', recipe=same_recipe, ingredients=clean_ingreds(same_recipe))

    # Make sure recipe found has ingredient list and instructions (surprisingly they don't always)
    elif recipe_ingredients == None or recipe_instructions == None:
        flash("That isn't a complete recipe, pick another.", 'negative')
        return redirect('search.html')

    else:
        # add to db if not there
        #number = session['cookbook-id']
        user = User.query.filter_by(username=session['username']).first()
        cookbook = Cookbook.query.filter_by(owner_id=user.id).first()
        print("####################" + str(cookbook.id))
        
        new_recipe = Recipe(recipe_name, str(recipe_ingredients), recipe_instructs, recipe_time, cookbook.id)
        new = True
        #db.session.add(new_recipe)
        #db.session.commit()        
   
        return render_template('recipe.html', recipe=new_recipe, ingredients=clean_ingreds(new_recipe), new=new)
    #return render_template('search.html', recipe_instr=json_data) 
"""
    recipe_instructions = recipe_info.recipe_info # call recipe_info variable within recipe_info module
    return render_template('search.html', recipe_instructions=recipe_instructions )
"""

# save recipe route
@app.route("/recipe-added", methods=['POST'])
def save_recipe():
    
    name = request.form['name']
    time = request.form['time']
    ingredients = request.form['ingredients']
    print(type(ingredients))
    # keeps format consistent for recipes manually entered
    if type(ingredients) == str:
        ingredients = ingredients.split()
   
    instructions = request.form['instructions']

    user = getUserByName(session['username'])
    c_book = Cookbook.query.filter_by(owner_id=user.id).first()
    #print(type(session['cookbook-id']))
    print("###############################" + user.username)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" + str(c_book.id))
    #print("#############################" + str(session['cookbook-id']))

    same_recipe = Recipe.query.filter_by(name=name, instructions=instructions).first()
    if same_recipe:
        new_recipe = Recipe(same_recipe.name, same_recipe.ingredients, same_recipe.instructions, c_book.id)
        # makes a new Recipe with same stuff for this users cookbook    
        db.session.add(new_recipe)
        db.session.commit()

        flash("Recipe saved!", 'positive')
        return render_template('search.html')
    new_recipe = Recipe(name, str(ingredients), instructions, time, c_book.id)
    db.session.add(new_recipe)
    db.session.commit()

    flash("Recipe saved!", 'positive')
    return render_template('search.html')
    # TODO return user to calendar instead of search
    # user = getUserByName(session['username'])
    # events = getUsersEvents(session['username'])
    # return render_template('full-calendar.html', user=user, events=events, other_users=all_users, calendar_shown=user_name)


# display recipe instructions in modal
@app.route("/modal-recipe", methods=['POST'])
def display_modal_recipe():

    print("######################")
    recipe_name = request.form["recipe_name"]
    print(recipe_name)
    # recipe_name = content["recipe_name"]
    # print(recipe_name)
    print("##################")
    print("ok I got the recipe", recipe_name)
    print("######################")
    """ diplays recipe by id with normalized data in clean format """
    recipe = Recipe.query.filter_by(name=recipe_name).first()
    print(recipe)
    return render_template('recipe.html', recipe=recipe, ingredients=clean_ingreds(recipe))


@app.route("/recipe/<recipe_name>")
def display_recipe(recipe_name):
    """ diplays recipe by name with normalized data in clean format """
    recipe = Recipe.query.filter_by(name=recipe_name).first()
    return render_template('recipe.html', recipe=recipe, ingredients=clean_ingreds(recipe))


@app.route("/recipe-index")
def display_index():
    ''' displays list of all the recipes for that user '''
    recipes = getListUserRecipes(session['username'])
    return render_template('recipe-index.html', recipes=recipes, username=session['username'])

@app.route("/ingredients")
def display_ingredients():
    '''diplays a list of ingredients for recipes of all events'''
    #TODO need to clean up display AND place constraints eg(only next two weeks, none from past events) 
    user = User.query.filter_by(username=session['username']).first()
    meals = []
    events = get_meals_for_the_week(user.username)
    for event in events:
        meals.append(event.meal)
    recipes = []
    for meal in meals:
        recipes.append(Recipe.query.filter_by(name=meal).first())
    
    ingreds = []
    for recipe in recipes:
        nice_ings = clean_ingreds(recipe)
        # TODO use below to return list of ingredients without amounts or adjectives
        '''
        staples = get_nouns(recipe.ingredients)
        ingreds.append(staples)
        '''
        ingreds.append(nice_ings) 
    
    

    return render_template('ingredients.html', username=user.username, ingredients=ingreds, start=get_today_string(), end=get_week_from_string())


@app.route('/remove-meal', methods=['POST'])
def delete_meal_event():
    '''for now just removes event using dropdown form'''
    event_id = request.form['dinner_to_remove']
    # returns id as string from form
    ev_id = int(event_id)
    ev_to_get_id_from = Event.query.filter_by(id=ev_id).first()
    #use the event to get user  session['username'] not working here
    user_id = ev_to_get_id_from.user_id
    user = User.query.filter_by(id=user_id).first()
    # now that we've got the user identity we can delete event 
    Event.query.filter_by(id=event_id).delete()
    db.session.commit()
    
    events = getUsersEvents(user.username)
    write_events(events)
    recipes = Recipe.query.all()
    return render_template('full-calendar.html', user=user, events=events, recipes=recipes)

# @app.route('/other-calendars', methods=['POST'])
# def view_other_calendars():
#     ''' populates events.json with someones elses events by name'''
    
#     user = User.query.filter_by(username=session['username']).first()
#     user_name = request.form['other_cal_view']
#     other_events = getUsersEvents(user_name)
#     write_events(other_events)
#     return render_template('full-calendar.html', user=user, events=other_events, other_users=all_users, calendar_shown=user_name, no_remove=True)


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