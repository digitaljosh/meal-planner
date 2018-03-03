
from app import db 
from hashy import make_pw_hash 

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
    meal = db.Column(db.String(100), db.ForeignKey('recipe.name'))
    #meal = db.Column(db.Recipe)
    date = db.Column(db.String(10))
    #recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, date, user_id, meal=None):
        self.meal = meal
        self.date = date
        self.user_id = user_id

class Recipe(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), primary_key=True)# unique=True, nullable=False)
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

    

        



