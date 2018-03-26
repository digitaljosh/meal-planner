from application import db
from models import User, Event, Cookbook, Recipe, Api


db.create_all()

print("DB has been created!!")