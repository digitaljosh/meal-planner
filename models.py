
from app import db 
from hashy import make_pw_hash 

class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(db.Integer)
    requests = db.Column(db.Integer)
    last_api_call = db.Column(db.String(10))
    results_limit = db.Column(db.Integer)
    results_per_call = db.Column(db.Integer)
    requests_limit = db.Column(db.Integer)
    requests_per_call = db.Column(db.Integer)



    def __init__(self, results, requests, last_api_call, results_limit, results_per_call, requests_limit, requests_per_call):
        self.results = results
        self.requests = requests
        self.last_api_call = last_api_call
        self.results_limit = results_limit
        self.results_per_call = results_per_call
        self.requests_limit = requests_limit
        self.requests_per_call = requests_per_call



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    pw_hash = db.Column(db.String(100))
    email = db.Column(db.String(100))
    #calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))


    def __init__(self, username, password, email=None):
        self.username = username
        self.pw_hash = make_pw_hash(password)
        self.email = email


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.Integer, db.ForeignKey('recipe.id')) # used to be 'recipe name', now 'recipe id'
    #meal = db.Column(db.Recipe)
    date = db.Column(db.String(10))
    #recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meal_name = db.Column(db.String(100))

    def __init__(self, date, user_id, meal, meal_name):
        self.meal = meal
        self.date = date
        self.user_id = user_id
        self.meal_name = meal_name

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))# unique=True, nullable=False)
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


class Cookbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipes = db.relationship('Recipe', backref='cookbook')

    def __init__(self, owner_id):
        self.owner_id = owner_id

    

        



