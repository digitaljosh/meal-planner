import nltk
import unicodedata
import re

from fractions import Fraction


#TODO add plurals if we refactor get_measure without dropping s

list_of_measures = ['can', 'cup', 'cups', 'pint', 'quart', 'tablespoons', 'tablespoon', 'tbs', 'tb', 't', 'ts', 'teaspoon', 'tsps', 'gr',
                    'grams', 'gram','kilo', 'kilogram', 'dash', 'pinch', 'sprig', 'oz', 'ounce', 'ounces', 'cloves',
                    'lb', 'pound', 'pd']

words_not_recognized_as_nouns = ['flour', 'olive', 'oz']
'''
may need to nltk.download('punkt') and nltk.download('averaged_perception_tagger')
locally for each developer
'''

def get_nouns(ingredients_string): 
    ''' strips adjectives and amounts from ingredient return LIST'''
    ingredients = nltk.sent_tokenize(ingredients_string)
    nouns = []
    for ingredient in ingredients:
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(ingredient))):
            if word == 'flour' or word == 'oz' or word == 'olive':
                nouns.append(word)
            elif (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                nouns.append(word)
        
    return nouns

def obtain_measure(ingredient_string):
    ''' given an ingredient as a string extract the amount converts to float'''
    #TODO, enum class ?
    split_list_of_ingredient = ingredient_string.split()
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
                        try:
                            pattern = re.compile("\d+-\d+")
                            digits = []
                            if pattern.match(word):
                                value_range = pattern.match(word)
                                print(str(value_range.span()))
                                index_range = value_range.span()
                                value_string = word[index_range[0]:index_range[1]]
                                for item in value_string.split("-"):
                                    digits.append(item)
                                dig_sum = 0
                                for item in digits:
                                    dig_sum += int(item)
                                    
                                return dig_sum//2
                            
                        except TypeError:
                            pass
                            


def get_measure(ingredient):
    ''' parses the list for a noun that matches a unit of measure returns string of that noun'''
    nouns = get_nouns(ingredient)
    for noun in nouns:
        noun = noun.lower()
            # remove any 's', necessary for comparison onion is the same as onions
        # if noun[-1] == 's':
        #     noun = noun[:-1]
        
        if noun in list_of_measures: 
            return noun
        else:
            return ""


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
    ''' takes a list of ingredients and returns a dictionary of key=ingredient, value= number of ounces '''
    ingredient_dict = {}
    for ingredient in list_of_ingredients:
        amt = obtain_measure(ingredient)
        measurement = get_measure(ingredient)
        k_list = remove_amts_measures(ingredient)
        k_name = ' '.join(k_list)
        key_name= k_name.title() # thus parmesan == Parmesan == PARMESAN
        # in the case of say water or salt and pepper
        if amt == None:# and measurement == "whole":
            amt = 1
            measure = ""

        ingredient_dict[key_name] = [amt, measurement]

    return ingredient_dict


def make_shopping_list(list_of_lists_of_ingredients):
    ''' takes a list of list returns one dict with ingred as key '''
    big_dict_of_ingredients = {}
    for ingred_list in list_of_lists_of_ingredients:
        ingred_dict = make_ingredient_dict(ingred_list)
        for item in ingred_dict:
            if item in big_dict_of_ingredients:
                try:
                    big_dict_of_ingredients[item][0] += ingred_dict[item][0]
                except TypeError:
                    pass
            else:
                big_dict_of_ingredients[item] = ingred_dict[item]

    return big_dict_of_ingredients


def split_string_into_ngrams(string_x, number_for_n_ngram):
    sub_sects = nltk.ngrams(string_x.split(), number_for_n_ngram)
    grams = []
    for gram in sub_sects:
        grams.append(gram)
    return grams

def remove_amts_measures(string_x):
    '''should leave string with just nouns to parse for ngrams'''
    measure_to_remove = get_measure(string_x)
    noun_list = get_nouns(string_x)
    
    # BUG point can't remove because s has been dropped for comparisons
    try:
        #list(string_x).remove(measure_to_remove)
        noun_list.remove(measure_to_remove)
    except ValueError:
        # no measure to remove
        pass
    return noun_list




if __name__ == "__main__":
    y = chr(189) # 1/2
    z = chr(188) # 1/4
    weird_char = chr(8842)
    recipe_x = ['3 cups flour', '2 tbs butter', '1 egg', '1/2 cup sugar', '2.7 grams perwinkle pixie dust', str(y) + ' cups of almonds', weird_char + ' yogurt']
    recipe_y = ['1 cup flour', '3 tbs butter', '3 eggs', '3/4 cup sugar', '1.3 grams perwinkle dust', '3 pints water', '2 zebras']
    recipe_z = ['water', '2 bananas', str(z) + ' cups of almonds']


    lis_o_recipes = [recipe_x, recipe_y, recipe_z]
    print(str(lis_o_recipes))
    dict_head = make_shopping_list(lis_o_recipes)
    print(dict_head)
    print(dict_head['Flour']) #note keys are title case

    recipe_with_ranges = ['2-3 cups flour', '12-20 tbs butter', '1-5 kumquats']

    print(obtain_measure(str(recipe_with_ranges)))