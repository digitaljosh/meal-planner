
from app import db 
from hashy import make_pw_hash 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    #TODO hash password
    pw_hash = db.Column(db.String(100))
    email = db.Column(db.String(100))
    #calendar_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))


    def __init__(self, username, password, email=None):
        self.username = username
        self.pw_hash = make_pw_hash(password)
        self.email = email

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #TODO date object ?
    #month = db.Column(db.Integer[1-12])#
    year = db.Column(db.Integer) #DateTime
    #user_ids = db.relationship('User', backref='calendar')
    user_ids =  db.Column(db.Integer, db.ForeignKey('user.id'))
    dates = db.relationship('Day', backref='month')

    def __init__(self, year, user_ids):
        self.year = year 
        self.user_ids = user_ids

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(100))
    recipe = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    cal_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))

    def __init__(self, cal_id, meal=None):
        self.meal = meal
        self.cal_id = cal_id

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ingredients = db.Column(db.String(500))# maybe pickle to use a list ?
    instructions = db.Column(db.Text)# may also need to use pickled object 
    time = db.Column(db.Interval) # timedelta() time it take to perform task
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

        



