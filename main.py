
from flask import render_template, redirect, request,json, session, jsonify, flash
import requests
import json
import pprint 
import re 
import sqlalchemy
import io
import os
from datetime import date


from app import app, db
from hidden import mash_key
from models import User, Event, Recipe, Cookbook, Api
from hashy import check_pw_hash
from st_amts import make_shopping_list
from week_functs import get_today_string, get_week_from_string




#calendar demo copied with adjusts from https://gist.github.com/Nikola-K/37e134c741127380f5d6 


@app.before_request
def login_required():
    ''' makes sure user logged in to display calendar, not currently needed '''
    not_allowed_routes = ['cal_display',]
    if request.endpoint in not_allowed_routes and 'username' not in session:
        flash("You need to be logged in to see your calendar!", 'negative')
        return redirect('/')

# Original thought
# @app.route('/data')
# def return_data():
#     ''' Just displays the json events scheduled on calendar, plain text dev purposes only'''
#     with open("events.json", "r") as input_data:
#         # check out jsonfiy method or the built in json module
#         # http://flask.pocoo.org/docs/0.10/api/#module-flask.json
#         return input_data.read()

#New multiple data sources
@app.route('/data/<user_id>')
def return_user_event_data(user_id):
    ''' returns the data for that user's events.json '''
    print("$$")
    print(user_id)
    with open("events_" + str(user_id) + ".json", "r") as input_data:
        return input_data.read()

@app.route("/")
def index():
    return render_template('splash.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    ''' basic sign up page '''
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
            # just create a json file for user's events
            # maybe do this at login (?)


            
            '''
            filename = "events/" + str(new_user.id) + ".json"
            f = None 
            # checks if the file doesn't exists or if the file is empty
            if not os.path.isfile(filename) or os.stat(filename).st_size == 0:
                print("!!!!!!!!!!!!NO FILE!!!!!!!!!!!")
                print("CREATING")
                with open(filename, 'w') as json_file:
                    json_file.write(json.dumps({}))
            '''
            
            #     f = open(filename, "w")
            #     data = {"name": "Helio", "age": 88}

            #     print("No file Found, setting default age to", data["age"])
            #     json.dump(data, f)
            # if not f:  # open the file that exists now 
            #     f = open(filename) 
            #     data = json.load(f) 
            # f.close()  # close the file that was opened in either case 
            # with open("events/" + str(new_user.id) +".json", 'a') as new_file:
            #     json.dump({}, new_file)
            #     pass
            # set current session
            session['username'] = new_user.username
            session['cookbook-id'] = new_cookbook.id
            # since new user no events yet
            events = []
            # entered at login =>Event.write_events(events, new_user.id)
            return render_template('full-calendar.html', user= User.getUserByName(session['username']), events=events)      

@app.route('/login', methods=['GET', 'POST'])
def login():

    
    # seed api table if empty
    api_object = Api.query.filter_by(id=1).first()
    if api_object == None:
        today_string = date.today()
        api_seed = Api(0, 0, today_string)
        db.session.add(api_seed)
        db.session.commit()

    if request.method == 'GET':
        try:
            if session['username']:
                name = session['username']
                user = User.getUserByName(name)
                recipes = User.getListUserRecipes(name)
                # with open("events.json", "r") as input_data:
                #    evs = User.getUsersEvents(name)
                evs = User.getUsersEvents(name)
                Event.write_events(evs, user.id)
                return render_template('full-calendar.html', user=User.getUserByName(name), recipes=recipes, data_user_id=user.id)
                    # if len(input_data.read()) == 0:
                    #     evs = User.getUsersEvents(name)
                    #     # writes to events.json
                    #     Event.write_events(evs)
                    #     return render_template('full-calendar.html', user=User.getUserByName(name), recipes=recipes)
                    # else:
                    #     return render_template('full-calendar.html', user=User.getUserByName(name), recipes=recipes)
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
                evs = User.getUsersEvents(tried_name)
                # writes to events.json
                Event.write_events(evs, user.id)
                return redirect('/full-calendar')
            else:
                flash("Nice try!", 'negative')
                return redirect('/login')
        else:
            flash("Either you mistyped your username or you don't have an account.", 'negative')
            return render_template('login.html')



@app.route('/full-calendar', methods=['POST', 'GET'])
def cal_display():
    ''' Displays calendar as populated by user's events'''
    user = User.getUserByName(session['username'])
   
    if request.method == 'GET':
        # simply displays events in current state
        events = User.getUsersEvents(user.username)
        # strips events of those that have passed
        current_events = User.make_users_events_current(user.username)
        Event.write_events(current_events, user.id)
        recipes = User.getListUserRecipes(user.username)
        
        return render_template('full-calendar.html', user=user, events=events, recipes=recipes, data_user_id=user.id)
    else: # 'POST'
        # displays calendar with updated changes
        recipes = User.getListUserRecipes(user.username)
        if recipes == []:
            flash("Add some recipes to your cookbook.", 'negative')
            # no need to pass data_user_id since there's no events possible
            return render_template('full-calendar.html', user=user, recipes=recipes)

        date = request.form['date']
        recipe_id = request.form['meal']

        cookBook = Cookbook.query.filter_by(owner_id=user.id).first()
        recipe = Recipe.query.filter_by(id=recipe_id).filter_by(cookbook_id=cookBook.id).first()
        
        new_event = Event(meal=recipe_id, date=date, user_id=user.id, meal_name=recipe.name)
        db.session.add(new_event)
        db.session.commit()

        # retrieve the events from updated db
        User.make_users_events_current(user.username) # keeps users from adding events to the past
        event_list = Event.query.filter_by(user_id=user.id).all()
        Event.write_events(event_list, user.id)
        return render_template('full-calendar.html', events=event_list, user=user, recipes=recipes, data_user_id=user.id)




# TODO assign an admin user that can bypass api limits (if session[username]=admin => override api limits)
# TODO reset results and requests in db every 24 hours
# TODO consider lowering search results (currently @ 20) to extend daily search limits. Currently limited to 25 searches/day
# TODO may want to separate out the api call to a separate function




# GET Search Recipes - spoonacular
# costs 1 request per search
# costs 20 results per search (or however many recipes are returned)
@app.route('/search', methods=['POST', 'GET'])
def recipe_search():

    # check today's date against last api call, if not same day, reset results & requests in db
    today = date.today()
    api_obj = Api.query.filter_by(id=1).first()
    if str(today) != str(api_obj.last_api_call):
        # check to see if db has already been reset for the day
        if api_obj.results != 0:
            api_obj.results = 0
            api_obj.requests = 0
            db.session.commit()
    
    
    if request.method == 'POST':
        '''
        The following calls spoonacular api
        '''

        # get api object from db
        api_obj = Api.query.filter_by(id=1).first()
        
        # check if we have reached api call limits
        if api_obj.requests < 50 and api_obj.results < 500: 
            # if no limits reached, proceed with api call
            search_query = request.form['search']
            search_query = search_query.replace(" ","+")
            api = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&number=20&query="
            url = api + search_query
            headers={
                "X-Mashape-Key": mash_key,
                "Accept": "application/json"
                }

            json_data = requests.get(url, headers=headers).json()

            # make sure Jinja doesn't break if no recipe 
            if json_data['totalResults'] == 0:
                flash("No recipe listed, maybe check spelling and try again.", 'negative')
                return render_template('search.html')
            else:
                # creates variables for current results, current requests, and last-api-call to update data in db 
                current_results = api_obj.results + 20
                current_requests = api_obj.requests + 1
                last_api_call = date.today()                                

                # update api table then return search results
                api_obj.results = current_results
                api_obj.requests = current_requests
                api_obj.last_api_call = last_api_call
                db.session.commit()
                return render_template('search.html', recipe_list=json_data)
            
        else:

            # api call limit bypass for admin
            if session['username'] == 'admin':
                print("$#$#$#$#$ !!!!!!!! ADMIN FOR THE WIN  $#$#$#$ !!!!!!!")
                search_query = request.form['search']
                search_query = search_query.replace(" ","+")
                api = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&number=20&query="
                url = api + search_query
                headers={
                    "X-Mashape-Key": mash_key,
                    "Accept": "application/json"
                    }

                json_data = requests.get(url, headers=headers).json()

                # make sure Jinja doesn't break if no recipe 
                if json_data['totalResults'] == 0:
                    flash("No recipe listed, maybe check spelling and try again.", 'negative')
                    return render_template('search.html')
                else:
                    return render_template('search.html', recipe_list=json_data)
            else:
                # api call limit reached, deny api call and flash message
                flash("API limit reached. Login as admin to bypass.", 'negative')
                return render_template('search.html')
            
        
        

    else: # ie GET
        return render_template('search.html')


# Get Recipe Information - spoonacular API 
# costs 1 request
@app.route('/instructions', methods=['POST', 'GET'])
def recipe_instructions():

    '''
    The following code block calls spoonacular api
    '''
    
    # get api object from db
    api_obj = Api.query.filter_by(id=1).first()
        
    # check if we have reached api call limits
    if api_obj.requests < 50:

        # if no limits reached, proceed with api call
        recipe_id = request.args.get('id')
        api_part1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
        api_part2 = "/information?includeNutrition=false"
        url = api_part1 + recipe_id + api_part2
        headers={
        "X-Mashape-Key": mash_key,
        "Accept": "application/json"
        }

        json_data = requests.get(url, headers=headers).json()

        recipe_name = json_data['title']

        ingreds = json_data['extendedIngredients']

        recipe_ingredients = []
        for i in range(0, len(ingreds)):
            recipe_ingredients.append(ingreds[i]['originalString'])

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
            user = User.getUserByName(session['username'])
            cookbook = Cookbook.query.filter_by(owner_id=user.id).first()
            
            new_recipe = Recipe(recipe_name, str(recipe_ingredients), recipe_instructs, recipe_time, cookbook.id)
            new = True
            #not adding to db yet        
            # creates variables for current requests and last-api-call to update data in db 
            current_requests = api_obj.requests + 1
            last_api_call = date.today()                                

            # update api columns in api table then return search results
            api_obj.requests = current_requests
            api_obj.last_api_call = last_api_call
            db.session.commit()

            return render_template('recipe.html', recipe=new_recipe, ingredients=new_recipe.clean_ingreds(), new=new)
    
    else:
        if session['username'] == 'admin':
            # call api
            pass
        else:
            flash("API recipe instructions limit reached.Login as admin to bypass.", 'negative')
            return render_template('search.html')
        # displays recipe for user to decide if they'd like to save
        
        user - User.getUserByName(session['username'])
        cookbook = Cookbook.query.filter_by(owner_id=user.id).first()
        new_recipe = Recipe(recipe_name, str(recipe_ingredients), recipe_instructs, recipe_time, cookbook.id)
        new = True       
   
        return render_template('recipe.html', recipe=new_recipe, ingredients=new_recipe.clean_ingreds(), new=new)

# save recipe route
@app.route("/recipe-added", methods=['POST'])
def save_recipe():
    name = request.form['name']
    time = request.form['time']
    ingredients = request.form['ingredients']
    instructions = request.form['instructions']

    user = User.getUserByName(session['username'])
    events = User.getUsersEvents(user.username)
    

    if time == "":
        #defaults to 30 minutes
        time = 30

    # following elif no longer needed -changed time input type to 'number' so it only allows numbers
    #elif type(time) != int:
        #time = 30
   
    # keeps format consistent for recipes manually entered
    
    if type(ingredients) == str and '[' not in ingredients :
        ingredients = ingredients.splitlines()
      
    c_book = Cookbook.query.filter_by(owner_id=user.id).first()
    same_recipe = Recipe.query.filter_by(name=name, instructions=instructions, cookbook_id=c_book.id).first()
    if same_recipe:
        recipes = User.getListUserRecipes(session['username'])
        user = User.getUserByName(session['username'])
        flash("That recipe already exists", 'negative')   
        return render_template('full-calendar.html', user=user, events=events, recipes=recipes, data_user_id=user.id)

    new_recipe = Recipe(name, str(ingredients), instructions, str(time), c_book.id)
    db.session.add(new_recipe)
    db.session.commit()

    recipes = User.getListUserRecipes(session['username'])
    flash("Recipe saved!", 'positive')
    return render_template('full-calendar.html', user=user, events=events, recipes=recipes)


@app.route("/remove-recipe", methods=['POST'])
def delete_recipe():
    recipe_id = request.form["id"]
    #need to remove any event with that recipe first
    events_to_go = Event.query.filter_by(meal=recipe_id).all()
    for event in events_to_go:
        Event.query.filter_by(id=event.id).delete()

    Recipe.query.filter_by(id=recipe_id).delete()
    db.session.commit()

    recipes = User.getListUserRecipes(session['username'])
    return render_template('recipe-index.html', recipes=recipes, username=session['username'])
    

# display recipe instructions in modal
@app.route("/modal-recipe", methods=['POST'])
def display_modal_recipe():
    ''' displays the recipe '''
    recipe_date = request.form["recipe_date"]
    username = session['username']

    user = User.getUserByName(username)
    event = Event.query.filter_by(date=recipe_date).filter_by(user_id=user.id).first()
    event_meal_id = event.meal
    recipe = Recipe.query.filter_by(id=event_meal_id).first()

    return render_template('recipe.html', recipe=recipe, recipe_date=recipe_date, ingredients=recipe.clean_ingreds())

@app.route("/recipe/<recipe_id>")
def display_recipe(recipe_id):
    """ diplays recipe by name with normalized data in clean format """
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    button_flag = True
    return render_template('recipe.html', recipe=recipe, button_flag=button_flag, ingredients=recipe.clean_ingreds())


@app.route("/recipe-index")
def display_index():
    ''' displays list of all the recipes for that user '''
    recipes = User.getListUserRecipes(session['username'])
    return render_template('recipe-index.html', recipes=recipes, username=session['username'])

@app.route("/ingredients")
def display_ingredients():
    '''diplays a list of ingredients for recipes of all events for that week'''
    user = User.getUserByName(session['username'])
    # gets events for week, could change or make a user input
    events = User.get_meals_for_the_week(user.username)

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
    user = User.getUserByName(username)
    
    Event.query.filter_by(date=event_date).filter_by(user_id=user.id).delete()
    db.session.commit()
    
    events = User.getUsersEvents(user.username)
    Event.write_events(events, user.id)
   
    recipes = User.getListUserRecipes(username)

    return render_template('full-calendar.html', user=user, events=events, recipes=recipes, data_user_id=user.id)

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