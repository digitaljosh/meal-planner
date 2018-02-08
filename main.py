from flask import Flask, render_template, request, json, request
#from rapidconnect import RapidConnect
import requests
import json

#from flask_sqlalchemy import SQLAlchemy 

#TODO break main apart into seperate files later
app = Flask(__name__)

#app.config['SQALCHEMY_DATABASE_URI'] = 'setup localhost phpmyadmin here'
#db = SQLAlchemy(app)


#app.config['SQLALCHEMY_ECHO'] = True 
app.config['DEBUG'] = True



#GET Search Recipes - spoonacular
@app.route('/search', methods=['POST', 'GET'])
def recipe_search():

    if request.method == 'POST':
        
        search_query = request.form['search']
        search_query = search_query.replace(" ","+")

        api = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?instructionsRequired=true&query="
        url = api + search_query
        headers={
            "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
            "Accept": "application/json"
            }

        json_data = requests.get(url, headers=headers).json()

        

        print("########################################")
        print("json_data Type: ")
        print(type(json_data))
        #print(json_data)
        print("########################################")


        return render_template('search.html', recipe_list=json_data)

    else:
        return render_template('search.html')



# Get Recipe Information - spoonacular API 
@app.route('/instructions', methods=['POST', 'GET'])
def recipe_instructions():
    recipe_id = request.args.get('id')
    api_part1 = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/"
    api_part2 = "/information?includeNutrition=false"
    url = api_part1 + recipe_id + api_part2
    headers={
    "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
    "Accept": "application/json"
    }

    json_data = requests.get(url, headers=headers).json()


    print("######################")
    print(type(json_data))
    print(json_data)
    print("######################")


    
    return render_template('search.html', recipe_instr=json_data) 



@app.route("/")
def index():

    return render_template('splash.html')

@app.route('/login')
def login():
    return render_template('/login.html')

@app.route('/sign-up')
def signup():
    return render_template('/sign-up.html')

if __name__ == '__main__':
    app.run()