'''
#from main import db 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    #TODO hash password
    pw = db.Column(db.Sting(100))
    email = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.email = email

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #TODO date object ?
    month = db.Column(db.Integer[1-12])#?
    year = db.Column(db.Integer)
    user_id(s) =  db.Column(db.Integer, db.ForeighKey('user.id'))
    dates = db.relationship('Day', backref='month')

    def __init__(self, month, year, dates):
        self.date = month, year #?
        self.user_id(s) = user_id(s)

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(100))
    recipe = db.Column(db.Integer, db.ForeginKey('recipe.id'))
    cal_id = db.Column(db.Integer, db.ForeignKey('calendar.id'))

    def __init__(self, meal=None, cal_id)
        self.meal = meal
        self.cal_id = cal_id

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ingredients = db.Column(db.ARRAY(String(50)))
    instructions = db.Column(db.Text)
    time = db.Column(Time)

    def __init__(self, name, ingredients, instructions, time):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.time = time

'''
        



