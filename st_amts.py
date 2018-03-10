import nltk
import re
import unicodedata
from fractions import Fraction



list_of_measures = ['can', 'cup', 'pint', 'quart', 'tablespoon', 'tb', 't', 'ts', 'teaspoon', 'tsp', 'gr',
                    'gram', 'kilo', 'kilogram', 'dash', 'pinch', 'sprig', 'oz', 'ounce']


'''
may need to nltk.download('punkt') and nltk.download('averaged_perception_tagger')
locally for each developer
'''
#TODO still need to look into ngrams olive oil, Jack Cheese, manicotti shells etc. 


def get_nouns(ingredients_string):
    ''' strips adjectives and amounts from ingredient '''
    ingredients = nltk.sent_tokenize(ingredients_string)
    nouns = []
    for ingredient in ingredients:
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(ingredient))):
         if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
             nouns.append(word)
        
    return nouns

def obtain_measure(ingredient):
    ''' given an ingredient as a string extract the amount converts to float'''
    
    split_list_of_ingredient = ingredient.split()
    for word in split_list_of_ingredient:
        try:
            num = int(word)
            #return float(num)
            return num
        except ValueError:
            try:
                fl = float(word)
                return fl
            except ValueError:
                try:
                    # adding a float to fraction forces Fraction to float
                    fr = Fraction(word)
                    fr += 0.0
                    return fr
                except ValueError:
                    # try and see if unicode
                    try: 
                        uni = ord(word)
                        # use unicode conversion function here
                        if uni in range(8528-8543) or uni == 188 or uni == 189 or uni == 190:
                            uni_fl = unicodedata.numeric(chr(uni))
                            return uni_fl 
                        else: pass
                    except TypeError:
                        pass



def get_measure(ingredient):
    ''' parses the string for a noun that matches a unit of measure'''
    nouns = get_nouns(ingredient)
    for noun in nouns:
        noun = noun.lower()
            # remove any 's', necessary for comparison onion is the same as onions
        if noun[-1] == 's':
            noun = noun[:-1]
        
        if noun in list_of_measures: 
            return noun
        else:
            return "whole"


def convert_amt_to_oz(measure, amt):
    ''' converts mesures into ounces for ease of conversion at future date?'''
    if measure == 'whole':
        # later we can use the if int conditional to test for whole foods
        return int(1)
    if measure == 'can':
        # use valueError later to test for cans vs ounce ampunts ?
        return "CAN"
    elif measure == 'cup':
        oz = amt * 8
        return oz
    elif measure == 'pint':
        oz = amt * 16
        return oz
    elif measure == 'tb':
        oz = amt * 0.5
        return oz
    elif measure == 'tsp':
        oz = amt * 0.16667
        return oz
    elif measure == 'gram':
        oz = amt * 0.035273


def convert_amt_to_metric(measure, amt):
    ''' converts american measures to metric grams '''
    return convert_amt_to_oz(measure, amt) * 28.3495



def make_ingredient_dict(list_of_ingredients):
    ''' tatkes a list of ingredients and returns a dictionary of key=ingredient, value= number of ounces '''
    ingredient_dict = {}
    for ingredient in list_of_ingredients:
        # flour is also a verb and ignored as noun by nltk
        if 'flour' in ingredient.lower():
            nouns = get_nouns(ingredient) + ['flour']
            measure = get_measure(ingredient)
        else:
            nouns = get_nouns(ingredient)
            measure = get_measure(ingredient)
       
        for noun in nouns:
            noun = noun.lower()
            # remove any 's', necessary for comparison onion is the same as onions
            if noun[-1] == 's':
                noun = noun[:-1]
        
            if noun not in list_of_measures:
                amt = obtain_measure(ingredient)
                '''
                print("++" + str(measure))
                print("--" + str(amt))
                print("==" + str(convert_amt_to_oz(measure, amt)))
                '''
                #below if simply using all
                #ingredient_dict[noun] = convert_amt_to_oz(measure, amt)

                # in the case of say water , but breaks adding value to dict since you can't add int and string
              
                if amt == None and measure == "whole":
                    amt = ""
                    measure = ""
                
                ingredient_dict[noun] = [amt, measure]

    return ingredient_dict

def make_shopping_list(*lists_of_ingredients):
    big_dict_of_ingredients = {}
    for ingreds in lists_of_ingredients:
        ingred_dict = make_ingredient_dict(ingreds)
        for item in ingred_dict:
            if item in big_dict_of_ingredients:
                try:
                    big_dict_of_ingredients[item][0] += ingred_dict[item][0]
                except TypeError:
                    pass
            else:
                big_dict_of_ingredients[item] = ingred_dict[item]

    return big_dict_of_ingredients




if __name__ == "__main__":
    y = chr(189) # 1/2
    z = chr(188) # 1/4
    weird_char = chr(8842)
    recipe_x = ['3 cups flour', '2 tbs butter', '1 egg', '1/2 cup sugar', '2.7 grams perwinkle pixie dust', str(y) + ' cups of almonds', weird_char + ' yogurt']
    recipe_y = ['1 cup flour', '3 tbs butter', '3 eggs', '3/4 cup sugar', '1.3 grams perwinkle dust', '3 pints water', '2 zebras']
    recipe_z = ['water', '2 bananas', str(z) + ' cups of almonds']

    print(recipe_z)
    #TODO need to make a copy of dict before reassigning values for display
    clean_dict = make_shopping_list(recipe_x, recipe_y, recipe_z)
    print(clean_dict)
    for k, v in clean_dict.items():
        if v[1] == 'whole':
            v[1] = ""
        print(k + " : " + str(v[0]) + " " + v[1])
    print(clean_dict)

    recipe_knee = ['2 cups water', '1/4 cup water', '3.5 grams water']
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(make_shopping_list(recipe_knee, recipe_knee, recipe_knee))
   