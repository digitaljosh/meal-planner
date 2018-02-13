#Get Recipe Information - spoonacular api
recipe_info = {  
   'vegetarian':False,
   'vegan':False,
   'glutenFree':False,
   'dairyFree':False,
   'veryHealthy':False,
   'cheap':False,
   'veryPopular':False,
   'sustainable':False,
   'weightWatcherSmartPoints':15,
   'gaps':'no',
   'lowFodmap':False,
   'ketogenic':False,
   'whole30':False,
   'servings':8,
   'preparationMinutes':15,
   'cookingMinutes':30,
   'sourceUrl':'http://thepioneerwoman.com/cooking/2010/12/chicken-and-dumplings/',
   'spoonacularSourceUrl':'https://spoonacular.com/chicken-and-dumplings-12348',
   'aggregateLikes':1,
   'spoonacularScore':47.0,
   'healthScore':10.0,
   'creditText':'The Pioneer Woman',
   'sourceName':'The Pioneer Woman',
   'pricePerServing':152.35,
   'extendedIngredients':[  
      {  
         'id':1009016,
         'aisle':'Beverages',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/apple-cider.jpg',
         'consistency':'solid',
         'name':'apple cider',
         'amount':0.5,
         'unit':'cup',
         'originalString':'1/2 cup Apple Cider',
         'metaInformation':[  

         ]
      },
      {  
         'id':18371,
         'aisle':'Baking',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/white-powder.jpg',
         'consistency':'solid',
         'name':'baking powder',
         'amount':1.0,
         'unit':'Tablespoon',
         'originalString':'1 Tablespoon (heaping) Baking Powder',
         'metaInformation':[  
            '()'
         ]
      },
      {  
         'id':1001,
         'aisle':'Milk, Eggs, Other Dairy',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg',
         'consistency':'solid',
         'name':'butter',
         'amount':2.0,
         'unit':'Tablespoons',
         'originalString':'2 Tablespoons Butter',
         'metaInformation':[  

         ]
      },
      {  
         'id':11124,
         'aisle':'Produce',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/carrots.jpg',
         'consistency':'solid',
         'name':'carrots',
         'amount':0.5,
         'unit':'cup',
         'originalString':'1/2 cup Finely Diced Carrots',
         'metaInformation':[  
            'diced',
            'finely'
         ]
      },
      {  
         'id':11143,
         'aisle':'Produce',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/celery.jpg',
         'consistency':'solid',
         'name':'celery',
         'amount':0.5,
         'unit':'cup',
         'originalString':'1/2 cup Finely Diced Celery',
         'metaInformation':[  
            'diced',
            'finely'
         ]
      },
      {  
         'id':20081,
         'aisle':'Baking',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/flour.png',
         'consistency':'solid',
         'name':'flour',
         'amount':0.5,
         'unit':'cup',
         'originalString':'1/2 cup All-purpose Flour',
         'metaInformation':[  
            'all-purpose'
         ]
      },
      {  
         'id':20081,
         'aisle':'Baking',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/flour.png',
         'consistency':'solid',
         'name':'flour',
         'amount':1.0,
         'unit':'cup',
         'originalString':'1-1/2 cup All-purpose Flour',
         'metaInformation':[  
            'all-purpose'
         ]
      },
      {  
         'id':11297,
         'aisle':'Produce',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/parsley.jpg',
         'consistency':'solid',
         'name':'fresh parsley',
         'amount':2.0,
         'unit':'Tablespoons',
         'originalString':'2 Tablespoons Minced Fresh Parsley (optional)',
         'metaInformation':[  
            'fresh',
            'minced'
         ]
      },
      {  
         'id':2042,
         'aisle':'Spices and Seasonings',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/thyme.jpg',
         'consistency':'solid',
         'name':'ground thyme',
         'amount':0.5,
         'unit':'teaspoon',
         'originalString':'1/2 teaspoon Ground Thyme',
         'metaInformation':[  

         ]
      },
      {  
         'id':1049,
         'aisle':'Milk, Eggs, Other Dairy',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/fluid-cream.jpg',
         'consistency':'solid',
         'name':'half & half',
         'amount':1.0,
         'unit':'cup',
         'originalString':'1-1/2 cup Half-and-half',
         'metaInformation':[  

         ]
      },
      {  
         'id':1053,
         'aisle':'Milk, Eggs, Other Dairy',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/fluid-cream.jpg',
         'consistency':'liquid',
         'name':'heavy cream',
         'amount':0.5,
         'unit':'cup',
         'originalString':'1/2 cup Heavy Cream',
         'metaInformation':[  

         ]
      },
      {  
         'id':1082047,
         'aisle':'Spices and Seasonings',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/salt.jpg',
         'consistency':'solid',
         'name':'kosher salt',
         'amount':1.0,
         'unit':'teaspoon',
         'originalString':'1 teaspoon Kosher Salt',
         'metaInformation':[  

         ]
      },
      {  
         'id':6970,
         'aisle':'Canned and Jarred',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/chicken-broth.png',
         'consistency':'liquid',
         'name':'low sodium chicken broth',
         'amount':6.0,
         'unit':'cups',
         'originalString':'6 cups Low Sodium Chicken Broth',
         'metaInformation':[  
            'low sodium'
         ]
      },
      {  
         'id':4053,
         'aisle':'Oil, Vinegar, Salad Dressing',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/olive-oil.jpg',
         'consistency':'liquid',
         'name':'olive oil',
         'amount':2.0,
         'unit':'Tablespoons',
         'originalString':'2 Tablespoons Olive Oil',
         'metaInformation':[  

         ]
      },
      {  
         'id':11282,
         'aisle':'Produce',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/brown-onion.jpg',
         'consistency':'solid',
         'name':'onion',
         'amount':1.0,
         'unit':'',
         'originalString':'1 whole Medium Onion, Finely Diced',
         'metaInformation':[  
            'diced',
            'whole',
            'medium',
            'finely'
         ]
      },
      {  
         'id':2047,
         'aisle':'Spices and Seasonings',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/salt.jpg',
         'consistency':'solid',
         'name':'salt',
         'amount':8.0,
         'unit':'servings',
         'originalString':'Salt As Needed',
         'metaInformation':[  
            'as needed'
         ]
      },
      {  
         'id':1102047,
         'aisle':'Spices and Seasonings',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/salt-and-pepper.jpg',
         'consistency':'solid',
         'name':'salt and pepper',
         'amount':8.0,
         'unit':'servings',
         'originalString':'Salt And Pepper',
         'metaInformation':[  

         ]
      },
      {  
         'id':2043,
         'aisle':'Spices and Seasonings',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/turmeric.jpg',
         'consistency':'solid',
         'name':'turmeric',
         'amount':0.25,
         'unit':'teaspoon',
         'originalString':'1/4 teaspoon Turmeric',
         'metaInformation':[  

         ]
      },
      {  
         'id':5006,
         'aisle':'Meat',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg',
         'consistency':'solid',
         'name':'whole chicken',
         'amount':1.0,
         'unit':'',
         'originalString':'1 whole Chicken, Cut Into Pieces (cut Up Fryer)',
         'metaInformation':[  
            'whole',
            'cut into pieces (cut up fryer)'
         ]
      },
      {  
         'id':35137,
         'aisle':'Ethnic Foods;Baking',
         'image':'https://spoonacular.com/cdn/ingredients_100x100/cornmeal.jpg',
         'consistency':'solid',
         'name':'yellow cornmeal',
         'amount':0.5,
         'unit':'cup',
         'originalString':'1/2 cup Yellow Cornmeal',
         'metaInformation':[  
            'yellow'
         ]
      }
   ],
   'id':12348,
   'title':'Chicken and Dumplings',
   'readyInMinutes':45,
   'image':'https://spoonacular.com/recipeImages/12348-556x370.jpg',
   'imageType':'jpg',
   'cuisines':[  

   ],
   'dishTypes':[  
      'lunch',
      'main course',
      'main dish',
      'dinner'
   ],
   'diets':[  

   ],
   'occasions':[  

   ],
   'winePairing':{  
      'pairedWines':[  

      ],
      'pairingText':'',
      'productMatches':[  

      ]
   },
   'instructions':'Sprinkle chicken pieces with salt and pepper, then dredge both sides in flour. Melt butter in a pot over medium-high heat. In two batches, brown chicken on both sides and remove to a clean plate. In the same pot, add diced onion, carrots, and celery. Stir and cook for 3 to 4 minutes over medium-low heat. Stir in ground thyme and turmeric, then pour in chicken broth and apple cider. Stir to combine, then add browned chicken. Cover pot and simmer for 20 minutes. While chicken is simmering, make the dough for the dumplings: sift together all dry ingredients, then add half-and-half, stirring gently to combine. Set aside. Remove chicken from pot and set aside on a plate. Use two forks to remove chicken from the bone. Shred, then add chicken to the pot. Pour heavy cream into the pot and stir to combine. Drop tablespoons of dumpling dough into the simmering pot. Add minced parsley if using. Cover pot halfway and continue to simmer for 15 minutes. Check seasonings; add salt if needed. Allow to sit for 10 minutes before serving. *Adapted from Gourmet Magazine',
   'analyzedInstructions':[  
      {  
         'name':'',
         'steps':[  
            {  
               'number':1,
               'step':'Sprinkle chicken pieces with salt and pepper, then dredge both sides in flour. Melt butter in a pot over medium-high heat. In two batches, brown chicken on both sides and remove to a clean plate. In the same pot, add diced onion, carrots, and celery. Stir and cook for 3 to 4 minutes over medium-low heat. Stir in ground thyme and turmeric, then pour in chicken broth and apple cider. Stir to combine, then add browned chicken. Cover pot and simmer for 20 minutes. While chicken is simmering, make the dough for the dumplings: sift together all dry ingredients, then add half-and-half, stirring gently to combine. Set aside.',
               'ingredients':[  
                  {  
                     'id':1102047,
                     'name':'salt and pepper',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/salt-and-pepper.jpg'
                  },
                  {  
                     'id':1005006,
                     'name':'chicken pieces',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/chicken-parts.jpg'
                  },
                  {  
                     'id':2042,
                     'name':'ground thyme',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/thyme.jpg'
                  },
                  {  
                     'id':1009016,
                     'name':'apple cider',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/apple-cider.jpg'
                  },
                  {  
                     'id':2043,
                     'name':'turmeric',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/turmeric.jpg'
                  },
                  {  
                     'id':11124,
                     'name':'carrot',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/carrots.jpg'
                  },
                  {  
                     'id':1025006,
                     'name':'chicken',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg'
                  },
                  {  
                     'id':1001,
                     'name':'butter',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg'
                  },
                  {  
                     'id':11143,
                     'name':'celery',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/celery.jpg'
                  },
                  {  
                     'id':20081,
                     'name':'all purpose flour',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/flour.png'
                  },
                  {  
                     'id':11282,
                     'name':'onion',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/brown-onion.jpg'
                  }
               ],
               'equipment':[  
                  {  
                     'id':404752,
                     'name':'pot',
                     'image':'https://spoonacular.com/cdn/equipment_100x100/stock-pot.jpg'
                  }
               ],
               'length':{  
                  'number':23,
                  'unit':'minutes'
               }
            },
            {  
               'number':2,
               'step':'Remove chicken from pot and set aside on a plate. Use two forks to remove chicken from the bone. Shred, then add chicken to the pot.',
               'ingredients':[  
                  {  
                     'id':1025006,
                     'name':'chicken',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg'
                  }
               ],
               'equipment':[  
                  {  
                     'id':404752,
                     'name':'pot',
                     'image':'https://spoonacular.com/cdn/equipment_100x100/stock-pot.jpg'
                  }
               ]
            },
            {  
               'number':3,
               'step':'Pour heavy cream into the pot and stir to combine. Drop tablespoons of dumpling dough into the simmering pot.',
               'ingredients':[  
                  {  
                     'id':1053,
                     'name':'heavy cream',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/fluid-cream.jpg'
                  }
               ],
               'equipment':[  
                  {  
                     'id':404752,
                     'name':'pot',
                     'image':'https://spoonacular.com/cdn/equipment_100x100/stock-pot.jpg'
                  }
               ]
            },
            {  
               'number':4,
               'step':'Add minced parsley if using. Cover pot halfway and continue to simmer for 15 minutes. Check seasonings; add salt if needed. Allow to sit for 10 minutes before serving. *Adapted from Gourmet Magazine',
               'ingredients':[  
                  {  
                     'id':11297,
                     'name':'parsley',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/parsley.jpg'
                  },
                  {  
                     'id':2047,
                     'name':'salt',
                     'image':'https://spoonacular.com/cdn/ingredients_100x100/salt.jpg'
                  }
               ],
               'equipment':[  
                  {  
                     'id':404752,
                     'name':'pot',
                     'image':'https://spoonacular.com/cdn/equipment_100x100/stock-pot.jpg'
                  }
               ],
               'length':{  
                  'number':25,
                  'unit':'minutes'
               }
            }
         ]
      }
   ],
   'creditsText':'The Pioneer Woman'
}