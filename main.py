
from flask import render_template, redirect, request,json, session, jsonify, flash
import requests
import json
import pprint 
import datetime
import re 
import sqlalchemy

from app import app, db
from models import User, Event, Recipe, Cookbook
from hashy import check_pw_hash
from st_amts import make_shopping_list
from data_functs import (clean_ingreds, getUserByName, getUsersEvents, write_events, 
                        make_users_events_current, get_meals_for_the_week, get_today_string,
                        get_week_from_string, getListUserRecipes)



#calendar demo copied with adjusts from https://gist.github.com/Nikola-K/37e134c741127380f5d6 


@app.before_request
def login_required():
    ''' makes sure user logged in to display calendar, not currently needed '''
    not_allowed_routes = ['cal_display',]
    if request.endpoint in not_allowed_routes and 'username' not in session:
        flash("You need to be logged in to see your calendar!", 'negative')
        return redirect('/')

@app.route('/data')
def return_data():
    ''' Just displays the json events scheduled on calendar dev purposes only'''
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
        elif len(p_word) < 6 or len(p_word) > 20:
            flash("Passwords must be at least 6 chars long, 20 at most.", "negative")
            return render_template('sign-up.html', username=name)
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
                name = session['username']
                recipes = getListUserRecipes(name)
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
        recipes = getListUserRecipes(user.username)
        
        return render_template('full-calendar.html', user=user, events=events, recipes=recipes)
    else: # 'POST'
        # displays calendar with updated changes
        recipes = getListUserRecipes(user.username)
        if recipes == []:
            flash("Add some recipes to your cookbook.", 'negative')
            return render_template('full-calendar.html', user=user, recipes=recipes)

        date = request.form['date']
        recipe_id = request.form['meal']

        cookBook = Cookbook.query.filter_by(owner_id=user.id).first()
        recipe = Recipe.query.filter_by(id=recipe_id).filter_by(cookbook_id=cookBook.id).first()
        
        new_event = Event(meal=recipe_id, date=date, user_id=user.id, meal_name=recipe.name)
        db.session.add(new_event)
        db.session.commit()

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
        api = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&number=20&query="
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
   
    '''Duplicates won't be allowed by db anyway so let them push a save button if they wish
    # Assumption here, FOR NOW, is that there won't be multiple recipes with the same name and exact same
    same_recipe = Recipe.query.filter_by(name=recipe_name, instructions=recipe_instructs).first()
   
    if same_recipe:
        #already in db, just display that one
        return render_template('recipe.html', recipe=same_recipe, ingredients=clean_ingreds(same_recipe))
    '''
    # Make sure recipe found has ingredient list and instructions (surprisingly they don't always)
    if recipe_ingredients == None or recipe_instructions == None:
        flash("That isn't a complete recipe, pick another.", 'negative')
        return redirect('search.html')

    else:
        # add to db if not there
        user = User.query.filter_by(username=session['username']).first()
        cookbook = Cookbook.query.filter_by(owner_id=user.id).first()
        
        new_recipe = Recipe(recipe_name, str(recipe_ingredients), recipe_instructs, recipe_time, cookbook.id)
        new = True
        #db.session.add(new_recipe)
        #db.session.commit()        
   
        return render_template('recipe.html', recipe=new_recipe, ingredients=clean_ingreds(new_recipe), new=new)


# save recipe route
@app.route("/recipe-added", methods=['POST'])
def save_recipe():
   
    name = request.form['name']
    time = request.form['time']
    ingredients = request.form['ingredients']
    instructions = request.form['instructions']

    user = getUserByName(session['username'])
    events = getUsersEvents(user.username)
   
    if time == "":
        #defaults to 30 minutes
        time = 30
    elif type(time) != int:
        time = 30
    
    # elif type(time) != int:
    #     flash("Sorry, times must be typed as number of minutes.", 'negative')
    #     #TODO not sure how to return modal
    #     return render_template('full-calendar.html', user=user, events=events)
   
    # keeps format consistent for recipes manually entered
    
    if type(ingredients) == str and '[' not in ingredients :
        ingredients = ingredients.splitlines()
      
    c_book = Cookbook.query.filter_by(owner_id=user.id).first()
    same_recipe = Recipe.query.filter_by(name=name, instructions=instructions, cookbook_id=c_book.id).first()
    if same_recipe:   
        return render_template('full-calendar.html', user=user, events=events)

    new_recipe = Recipe(name, str(ingredients), instructions, str(time), c_book.id)
    db.session.add(new_recipe)
    db.session.commit()

    recipes = getListUserRecipes(session['username'])
    flash("Recipe saved!", 'positive')
    return render_template('full-calendar.html', user=user, events=events, recipes=recipes)


@app.route("/remove-recipe", methods=['POST'])
def delete_recipe():
    recipe_id = request.form["id"]
    print(recipe_id)
    #need to remove any event with that recipe first
    events_to_go = Event.query.filter_by(meal=recipe_id).all()
    for event in events_to_go:
        Event.query.filter_by(id=event.id).delete()

    Recipe.query.filter_by(id=recipe_id).delete()
    db.session.commit()

    recipes = getListUserRecipes(session['username'])
    return render_template('recipe-index.html', recipes=recipes, username=session['username'])
    

# display recipe instructions in modal
@app.route("/modal-recipe", methods=['POST'])
def display_modal_recipe():
    ''' displays the recipe '''
    recipe_date = request.form["recipe_date"]
    username = session['username']

    user = getUserByName(username)
    event = Event.query.filter_by(date=recipe_date).filter_by(user_id=user.id).first()
    event_meal_id = event.meal
    recipe = Recipe.query.filter_by(id=event_meal_id).first()

    return render_template('recipe.html', recipe=recipe, recipe_date=recipe_date, ingredients=clean_ingreds(recipe))

@app.route("/recipe/<recipe_id>")
def display_recipe(recipe_id):
    """ diplays recipe by name with normalized data in clean format """
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    button_flag = True
    return render_template('recipe.html', recipe=recipe, button_flag=button_flag, ingredients=clean_ingreds(recipe))


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
    events = get_meals_for_the_week(user.username)

    ingredient_lists = []
    meals = []
    for event in events:
        meals.append(event.meal)
    for meal in meals:
        ready_for_dict = []
        recipe = Recipe.query.filter_by(id=meal).first()
        recipe_l = recipe.ingredients.split(',')
        ready_for_dict = []
        for ingred in recipe_l:
            ingred = ingred.replace(",", "").replace("[", "").replace("'", "").replace("]", "").strip()
            ready_for_dict.append(ingred)
        ingredient_lists.append(ready_for_dict)
        
    counted_ingredients = make_shopping_list(ingredient_lists)

    return render_template('ingredients.html', username=user.username, ingredients_dict=counted_ingredients, start=get_today_string(), end=get_week_from_string())


@app.route('/remove-meal', methods=['POST'])
def delete_meal_event():
    event_date = request.form['dinner_to_remove']
    username = session['username']
    user = getUserByName(username)
    
    Event.query.filter_by(date=event_date).filter_by(user_id=user.id).delete()
    db.session.commit()
    
    events = getUsersEvents(user.username)
    write_events(events)
   
    recipes = getListUserRecipes(username)

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