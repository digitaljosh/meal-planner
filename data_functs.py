import re
import json
import datetime
import nltk
from fractions import Fraction

from models import User, Event, Cookbook, Recipe
from app import db


def clean_ingreds(recipe):
        """splits recipe ingredients from list of one string to list of individual ingredient strings"""
        no_coma_ingreds = re.sub(',', '', recipe.ingredients)
        # splits from string of ingredients to list at first ' 
        ingreds = no_coma_ingreds.split(' \'')
        # remove brackets
        #ingreds = ings[1:-1]
        # below is to crop off last '
        fresh_ingredients = []
        for ingred in ingreds:
            #ingred = ingred[:-1]
            ingred = ingred.replace(",", "").replace("[", "").replace("'", "").replace("]", "")
            fresh_ingredients.append(ingred)
        return fresh_ingredients

def good_display_ingredients(list_of_ingredients):
    lists = list_of_ingredients.split(',')


def getUserByName(username):
    user = User.query.filter_by(username=username).first()
    return user

def getUsersEvents(username):
    user = getUserByName(username)
    events = Event.query.filter_by(user_id=user.id).all()
    return events

def getListUserRecipes(username):
    user = getUserByName(username)
    user_cookbook = Cookbook.query.filter_by(owner_id=user.id).first()
    #print("$$$$$$$$$$$$$$$$$$$$$$$$$$" + user_cookbook.recipes)
    recipes_list = user_cookbook.recipes
    for recipe in recipes_list:
         print("$$$$$$$$$$$$$$$$$$$$$$$$$$$" + recipe.name)
    # recipes = []
    # for  recipe_id in recipes_ids:
    #     recipes.append(Recipe.query.filter_by(id=recipe_id).first())
    #return recipe_list
    return user_cookbook.recipes


def write_events(events):
    """ overwrites event.json with current event list for current (session) user """
    with open('events.json', 'w') as event_list:
            #events.write('[')
            event_dicts = []
            for event in events:
                event_dicts.append({"title":event.meal, "start":event.date})
            event_list.write(json.dumps(event_dicts))
            #events.write(']') 


def make_users_events_current(username):
    ''' Drops events that have occured from table '''
    all_events = getUsersEvents(username)
    up_to_dates = []
    today = datetime.date.today()
    print(today)
    for event in all_events:
        date = datetime.datetime.strptime(event.date, "%Y-%m-%d").date()
        print(date)
        if date >= today:
        #if event.date > today:
            up_to_dates.append(event)
        else:
            Event.query.filter_by(id=event.id).delete()
            db.session.commit()

    return up_to_dates

def get_meals_for_the_week(username):
    ''' returns the events the user has planned for the next week '''
    week_events = []
    all_events = getUsersEvents(username)
    today = datetime.date.today()
    week_from_date = today + datetime.timedelta(days=7)
    for event in all_events:
        date = datetime.datetime.strptime(event.date, "%Y-%m-%d").date()
        if date >= today and date <= week_from_date:
            week_events.append(event)
    return week_events

def get_today_string():
    today_string = "{date:%m/%d}".format(date=datetime.datetime.now())
    return today_string

def get_week_from_string():
    today = datetime.datetime.today()
    week_from_date = today + datetime.timedelta(days=7)
    week_from = "{date:%m/%d}".format(date=week_from_date)
    return week_from

#TODO below need tweaking with ngrams perhaps
'''
may need to nltk.download('punkt') and nltk.download('averaged_perception_tagger')
locally for each developer
'''

def get_nouns(ingredients_string):
    ''' strips adjectives and amounts from ingredient '''
    ingredients = nltk.sent_tokenize(ingredients_string)
    nouns = []
    for ingredient in ingredients:
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(ingredient))):
         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
             nouns.append(word)
        
    return nouns

def ingredient_doubler(list_of_ingredients):
    new_ingredient_list = []
    for ingredient in list_of_ingredients:
        if ingredient not in new_ingredient_list:
            new_ingredient_list.append(ingredient)
        else:
            # ingredient already listed want to double the amount
            try:
                #returns first index number of match .start
                first_number_match_found = re.search("\d", ingredient)
                index = first_number_match_found.start()
                double = int(ingredient[index]) * 2
                ingredient[index] = str(double)
                new_ingredient = ingredient
            except AttributeError:
                # no digits found    
                new_ingredient = "2X" + ingredient
            # doubled = ingredient.replace(ingredient[x], ingredient[x*2])
            new_ingredient_list.replace(ingredient, new_ingredient)
            # new_ingredient_list[ingredient] = doubled
    return new_ingredient_list

    

def ingredients_doubler2(list_of_ingredients):
    new_ingredient_list = []
    for ingredient in list_of_ingredients:
        print("$$$$" + ingredient)
        if ingredient not in new_ingredient_list:
            print("+")
            new_ingredient_list.append(ingredient)
        else:
            print("-")
            # ingredient already listed want to double the amount
            try:
                #returns first index number of match .start
                first_number_match_found = re.search("\d", ingredient)
                index = first_number_match_found.start()
                double = int(ingredient[index]) * 2
                print('!!!' +ingredient[index])# = str(double)
                print("##############" + ingredient[index])
                new_ingredient = ingredient
            except AttributeError:
                # no digits found    
                new_ingredient = "2X" + ingredient
            # doubled = ingredient.replace(ingredient[x], ingredient[x*2])
            new_ingredient_list.replace(ingredient, new_ingredient)
            # new_ingredient_list[ingredient] = doubled
    #print(new_ingredient_list)
    return new_ingredient_list

    

def multiply_amts(list_of_ingredients, how_many_times_in_list):
    ''' if the ingredient is in the list it multiplies the amounts by how many times it occurs and returns updated string'''
    split_list_of_ingredients = list_of_ingredients.split()
    for word in split_list_of_ingredients:
        try:
            num = int(word)
            num *= how_many_times_in_list
            loc = split_list_of_ingredients.index(word)
            split_list_of_ingredients[loc] = str(num) 
        except ValueError:
            try:
                fl = float(word)
                fl *= how_many_times_in_list
                loc = split_list_of_ingredients.index(word)
                split_list_of_ingredients[loc] = str(fl)
            except ValueError:
                try:
                    fr = Fraction(word)
                    fr *=how_many_times_in_list 
                    loc = split_list_of_ingredients.index(word)
                    split_list_of_ingredients[loc] = str(fr)
                except ValueError:
                    pass

    return split_list_of_ingredients