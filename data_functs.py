import json
import datetime
import re

from models import User, Event, Cookbook, Recipe
from application import db


def clean_ingreds(recipe):
        """splits recipe ingredients from list of one string to list of individual ingredient strings"""
        no_coma_ingreds = re.sub(',', '', recipe.ingredients)
        # splits from string of ingredients to list at first ' 
        ingreds = no_coma_ingreds.split(' \'')
        # below is to crop off last '
        fresh_ingredients = []
        for ingred in ingreds:
            ingred = ingred.replace(",", "").replace("[", "").replace("'", "").replace("]", "")
            fresh_ingredients.append(ingred)
        return fresh_ingredients


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
   
    return user_cookbook.recipes


def write_events(events):
    """ overwrites event.json with current event list for current (session) user """
    with open('events.json', 'w') as event_list:
            event_dicts = []
            for event in events:
                event_dicts.append({"title":event.meal_name, "start":event.date, "id":event.meal})
            event_list.write(json.dumps(event_dicts))
            


def make_users_events_current(username):
    ''' Drops events that have occured from table '''
    all_events = getUsersEvents(username)
    up_to_dates = []
    today = datetime.date.today()
    for event in all_events:
        date = datetime.datetime.strptime(event.date, "%Y-%m-%d").date()
        if date >= today:
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

