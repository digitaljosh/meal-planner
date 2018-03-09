import nltk
import re
import unicodedata
from fractions import Fraction



list_of_measures = ['can', 'cup', 'pint', 'quart', 'tablespoon', 'tb', 'teaspoon', 'tsp', 'gr',
                    'gram', 'kilo', 'kilogram', 'dash', 'pinch']


'''
may need to nltk.download('punkt') and nltk.download('averaged_perception_tagger')
locally for each developer
'''
#TODO still need to look into ngrams chicken neck is currently being broken into chicken and neck


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
            return float(num)
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
                        uni_fl = unicodedata.numeric(chr(uni))
                        return uni_fl 
                    except TypeError:
                        pass



def get_measure(ingredient):
    
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
    elif measure = 'gram':
        oz = amt * 0.035273



def make_ingredient_dict(list_of_ingredients):
    ''' tatkes a list of ingredients and returns a dictionary of key=ingredient, value= number of ounces '''
    ingredient_dict = {}
    for ingredient in list_of_ingredients:
        nouns = get_nouns(ingredient)
        measure = get_measure(ingredient)
       
        for noun in nouns:
            noun = noun.lower()
            # remove any 's', necessary for comparison onion is the same as onions
            if noun[-1] == 's':
                noun = noun[:-1]
        
            if noun not in list_of_measures:
                amt = obtain_measure(ingredient)
                print("++" + str(measure))
                print("--" + str(amt))
                print("==" + str(convert_amt_to_oz(measure, amt)))
                ingredient_dict[noun] = convert_amt_to_oz(measure, amt)


    return ingredient_dict


if __name__ == "__main__":
    y = chr(189)
    x = ['3 cups flour', '2 tbs butter', '1 egg', '1/2 cup sugar', '2.7 grams perwinkle pixie dust', str(y) + ' cups of almonds']
    print(make_ingredient_dict(x))
