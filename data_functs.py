import re




def clean_ingreds(recipe):
        """splits recipe ingredients from list of one string to list of individual ingredient strings"""
        no_coma_ingreds = re.sub(',', '', recipe.ingredients)
        # splits from string of ingredients to list at first ' 
        ings = no_coma_ingreds.split(' \'')
        # remove brackets
        ingreds = ings[1:-1]
        # below is to crop off last '
        fresh_ingredients = []
        for ingred in ingreds:
            ingred = ingred[:-1]
            fresh_ingredients.append(ingred)
        return fresh_ingredients

# def good_display-ingredients(ingredients):
