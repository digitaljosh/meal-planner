import re
import json
import datetime

from models import User, Event
from app import db


def clean_ingreds(recipe):
        """splits recipe ingredients from list of one string to list of individual ingredient strings"""
        no_coma_ingreds = re.sub(',', '', recipe.ingredients)
        # splits from string of ingredients to list at first ' 
        ings = no_coma_ingreds.split(' \'')
        # remove brackets
        ingreds = ings[1:-1]
        # below is to crop off last '
        fresh_ingredients = []
        for ingred in ingreds:
            ingred = ingred[:-1]
            fresh_ingredients.append(ingred)
        return fresh_ingredients

# def good_display-ingredients(ingredients):


def getUserByName(username):
    user = User.query.filter_by(username=username).first()
    return user

def getUsersEvents(username):
    user = getUserByName(username)
    events = Event.query.filter_by(user_id=user.id).all()
    return events


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



        