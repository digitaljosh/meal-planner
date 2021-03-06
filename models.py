import datetime
import re
import json 

from app import db 
from hashy import make_pw_hash 

class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(db.Integer)
    requests = db.Column(db.Integer)
    last_api_call = db.Column(db.String(10))


    def __init__(self, results, requests, last_api_call):
        self.results = results
        self.requests = requests
        self.last_api_call = last_api_call
        



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    pw_hash = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, username, password, email=None):
        self.username = username
        self.pw_hash = make_pw_hash(password)
        self.email = email

    def getUserByName(name):
        return User.query.filter_by(username=name).first()

    def getUsersEvents(name):
        user = User.getUserByName(name)
        events = Event.query.filter_by(user_id=user.id).all()
        return events

    def getListUserRecipes(username):
        user = User.getUserByName(username)
        user_cookbook = Cookbook.query.filter_by(owner_id=user.id).first()
        return user_cookbook.recipes
    
    def make_users_events_current(username):
        ''' Drops events that have occured from table '''
        all_events = User.getUsersEvents(username)
        today = datetime.date.today()
        for event in all_events:
            date = datetime.datetime.strptime(event.date, "%Y-%m-%d").date()
            if date < today:
                Event.query.filter_by(id=event.id).delete()
                db.session.commit()
    

    def get_meals_for_the_week(username):
        ''' returns the events the user has planned for the next week '''
        week_events = []
        all_events = User.getUsersEvents(username)
        today = datetime.date.today()
        week_from_date = today + datetime.timedelta(days=7)
        for event in all_events:
            date = datetime.datetime.strptime(event.date, "%Y-%m-%d").date()
            if date >= today and date <= week_from_date:
                week_events.append(event)
        return week_events
        
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.Integer, db.ForeignKey('recipe.id')) 
    date = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meal_name = db.Column(db.String(100))

    def __init__(self, date, user_id, meal, meal_name):
        self.meal = meal
        self.date = date
        self.user_id = user_id
        self.meal_name = meal_name


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ingredients = db.Column(db.Text)# maybe pickle to use a list ?
    instructions = db.Column(db.Text)# may also need to use pickled object, might be okay though
    time = db.Column(db.Integer) # time in minutes
    cookbook_id = db.Column(db.Integer, db.ForeignKey('cookbook.id'))

    def __init__(self, name, ingredients, instructions, time, cookbook_id):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.time = time
        self.cookbook_id = cookbook_id

    def clean_ingreds(self):
        '''splits recipe ingredients from list of one string to list of individual ingredient strings'''
        no_coma_ingreds = re.sub(',', '', self.ingredients)
        # splits from string of ingredients to list at first ' 
        ingreds = no_coma_ingreds.split(' \'')
        # below is to crop off last '
        fresh_ingredients = []
        for ingred in ingreds:
            ingred = ingred.replace(",", "").replace("[", "").replace("'", "").replace("]", "")
            fresh_ingredients.append(ingred)
        return fresh_ingredients


    def clean_instructs(self):
        '''removes digits if present and splits string at periods to form list of strings'''

        # remove step numbers (digits) if present since they are not ubiquitous in api recipes. Step nums added in template view
        instructions = re.sub("\d+\.", "", self.instructions)
        
        # removes html tags
        instructions = re.sub("<.*?>", "", instructions)

        # splits string at "." and casts it as list
        instructions = instructions.split(".")

        # handles cases where parentheses exist in instructions
        fresh_instructions = []
        for step in instructions:
            step = step.replace("(", "").replace(")", "").replace("!", "")
            fresh_instructions.append(step)  

        # removes empty strings in list
        fresh_instructions = list(filter(None, fresh_instructions))

        return fresh_instructions


class Cookbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipes = db.relationship('Recipe', backref='cookbook')

    def __init__(self, owner_id):
        self.owner_id = owner_id

    

        



