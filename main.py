from flask import Flask, render_template, request, json
#from rapidconnect import RapidConnect
import requests
#from flask_sqlalchemy import SQLAlchemy 

#TODO break main apart into seperate files later
app = Flask(__name__)

#app.config['SQALCHEMY_DATABASE_URI'] = 'setup localhost phpmyadmin here'
#db = SQLAlchemy(app)


#app.config['SQLALCHEMY_ECHO'] = True 
app.config['DEBUG'] = True


@app.route('/search', methods=['POST', 'GET'])
def recipe_search():

    if request.method == 'POST':
        search_query = request.form['search']
        search_query = search_query.replace(" ","+")
        api = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?query="
        url = api + search_query
        headers={
            "X-Mashape-Key": "2lZIhttKlzmshfcvdDIws3dS8XAfp1Z9kkVjsn6Y7YuGocYKNB",
            "Accept": "application/json"
            }

        json_data = requests.get(url, headers=headers).json()
        

        print("########################################")
        title = json_data['results'][0]['title']
        print(title)
        print(type(title))
        print(type(json_data))


        print("########################################")
            
        
        ''' # making list of titles from json data
        recipe_list = []
        for recipe in json_data['results']:
            recipe_list.append(recipe['title'])
        '''

        print("########################################")
        #print(json_data)
        print("########################################")


        return render_template('search.html', recipe_list=json_data)

    else:
        return render_template('search.html')




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