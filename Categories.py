# out = open("out.txt", mode="w")
# input = open("lables.txt", mode="r").readlines()
#
# out.write("sort these:\n")
# for i in range(0, len(input)):
#     if i > 0 and i % 20 == 0:
#         out.write("]\n"
#                   "into these categories:\n"
#                   "[Fruit and Vegetables, Organic, Meat, Vegan & Vegetarian, Sauces and Dressings, Bulk Buys, Fish and Seafood, Butter & Spreads, Dairy and Eggs, Deli, Drinks, Easy Meals, Bakery, Kids, Pets, Cleaning, Personal Care, Snacks, Baking, Frozen, Alcoholic, Pantry, Other]\n"
#                   "In json format\n"
#                   "\n\n"
#                   "sort these:\n"
#                   "[")
#     out.write(input[i].replace("\n", "") + ", ")
#
# out.write("]\n"
#           "into these categories:\n"
#           "[Fruit and Vegetables, Organic, Meat, Vegan & Vegetarian, Sauces and Dressings, Bulk Buys, Fish and Seafood, Butter & Spreads, Dairy and Eggs, Deli, Drinks, Easy Meals, Bakery, Kids, Pets, Cleaning, Personal Care, Snacks, Baking, Frozen, Alcoholic, Pantry, Other]\n"
#           "In json format\n"
#           )

d1 = {
    "Fruit and Vegetables": ["Fresh Fruit", "Fresh Salad & Herbs", "Fresh Vegetables", "In Season",
                             "Prepared Fruit & Veg", "The Odd Bunch", "Fruit & Vegetables", "Fresh Cut Fruit",
                             "Fresh Herbs", "PrePacked Fresh Fruit", "PrePacked Fresh Vegetables", "Salad Bags"],
    "Organic": ["Organic"],
    "Meat": ["Meat", "BBQ Meat", "Beef", "Chicken & Poultry"],
    "Other": ["Shop Fresh Deals"]
}

d2 = {
    "Meat": ["Lamb", "Mince & Patties", "Offal & Bones", "Pork", "Roast Meat", "Sausages", "Venison & Game", "Butchery",
             "Fresh Beef & Lamb", "Fresh Chicken & Poultry", "Fresh Pork", "Fresh Sausages",
             "Fresh Venison & Game Meat", "PreCooked Sausages", "PrePacked Beef & Lamb", "PrePacked Chicken & Poultry",
             "PrePacked Sausages", "Bacon", "Continental Sausage & Salami", "Ham & Pork"],
    }

d3 = {
    "Meat": [
        "PreCooked Beef & Lamb",
        "PreCooked Chicken & Poultry"
    ],
    "Vegan & Vegetarian": [
        "Vegan & Vegetarian",
        "Vegan",
        "Pams Plant Based",
        "Vegan range",
        "Meat Free",
        "Frozen Vegetarian",
        "Vegetarian",
        "Dairy & Lactose Free",
        "Plant based alternatives"
    ],
    "Sauces and Dressings": [
        "sauces and Dressings",
        "Condiments & Dressings",
        "Aioli",
        "Barbeque Sauces",
        "Chilli & Pepper Sauces",
        "Chutneys",
        "Fruit Sauces",
        "Mayonnaise"
    ],
    }

d4 = {
    "Sauces and Dressings": [
        "Mint Sauces",
        "Mustards",
        "Salad Dressings",
        "Worcestershire Sauces",
        "Sauces & Pastes",
        "Sauces Stock & Marinades",
        "Chilled Pasta Sauces",
        "Marinades",
        "Packet Sauces",
        "Pasta Sauces",
        "Simmer & Stir-Through Sauces",
        "Soy Sauce",
        "Specialty Sauces",
        "Stir Fry Sauces"
    ],
    "Bulk Buys": [
        "Bulk Buys",
        "Bulk Foods",
        "Bulk & Loose Foods",
        "Bulk Breakfast Cereals",
        "Bulk Confectionery"
    ],
    "Pantry": [
        "Sauces & Pastes",
        "Soy Sauce",
        "Pasta Sauces",
    ],
    }

d5 = {
    "Bulk Buys": [
        "Bulk Dried Fruit",
        "Bulk Nuts",
        "Bulk Seeds Legumes & Grains",
        "Bulk Snacks & Mixes"
    ],
    "Fish and Seafood": [
        "Fish and Sea Food",
        "Fresh Fish",
        "Prawns & Seafood",
        "Salmon",
        "Seafood",
        "Fresh Fish Fillets & Steaks",
        "Fresh Seafood",
        "Fresh Shellfish",
        "Fresh Smoked Fish",
        "Frozen Fish & Seafood",
        "Seafood Salad"
    ],
    "Butter & Spreads": [
        "Butter & Spreads",
        "Dips Hummus & Nibbles",
        "Dips Pesto & Pate"
    ],
    "Frozen": [
        "Frozen Fish & Seafood"
    ],
    }

d6 = {
    "Organic": [
        "Fresh Organic Milk"
    ],
    "Sauces and Dressings": [
        "Dips & Salsas"
    ],
    "Butter & Spreads": [
        "Hummus",
        "Jams Honey & Spreads",
        "Honey",
        "Jam & Marmalade",
        "Marmite & Vegemite",
        "Nut Spreads",
        "Savoury Spreads",
        "Sweet Spreads"
    ],
    "Dairy and Eggs": [
        "Dairy and Eggs",
        "Cheese",
        "Long Life Milk",
        "Milk & Cream",
        "Yoghurt & Desserts",
        "Eggs",
        "Flavoured Milk",
        "Fresh Cream",
        "Fresh Milk",
        "Fresh Organic Milk"
    ],
    }

d7 = {
    "Dairy and Eggs": [
        "Long Life Milk & Milk Powder",
        "Sour Cream & Crème Fraiche",
        "Yoghurt & Dairy Food",
        "Yoghurt Bases",
        "Cheese Blocks",
        "Cheese Slices",
        "Cottage Cheese",
        "Cream Cheese",
        "Grated Cheese",
        "Specialty Cheeses"
    ],
    "Deli": [
        "Deli",
        "Deli Meats & Seafood",
        "Deli Salads",
        "Fresh Deli Savouries",
        "Deli Salads & Cooked Meats",
        "Deli Meats",
        "Deli Cheeseboards",
        "Deli Specialty Cheeses"
    ],
    "Drinks": [
        "Drinks",
        "Juice & Drinks"
    ],
    "Pantry": [
        "Long Life Milk & Milk Powder"
    ],
    }
d8 = {
    "Drinks": ["Low & no alcohol", "Coffee", "Juice & Cordial", "Soft Drinks & Sports Drinks", "Tea & Milk Drinks",
               "Water", "Cold Drinks", "Hot Drinks", "Black Teas", "Chai Teas", "Chocolate Milk Drink Mixes",
               "Coffee Additives & Filters", "Coffee Capsules", "Coffee Flavoured Sachets", "Fresh Coffees",
               "Fruit & Herbal Teas", "Green Teas", "Instant Coffees", "Malt Milk Drink Mixes"],
    "Easy Meals": ["Easy Meals"],
    }

d9 = {
    "Easy Meals": [
        "Fresh Pastas",
        "Instant Rices",
        "Rice Meals"
    ],
    "Bakery": [
        "Ice Cream Cones & Wafers",
        "Bakery",
        "Bagels Crumpets & Pancakes",
        "Baked In Store",
        "Buns Rolls & Bread Sticks",
        "Cakes Muffins & Desserts",
        "Gluten Free Bakery",
        "Low Carb & Keto Bakery",
        "Pastries Croissants & Biscuits",
        "Sliced & Packaged Bread",
        "Wraps Pita & Pizza Bases",
        "Hot Cross Buns",
        "Fresh Foods & Bakery",
        "Bakery",
        "Biscuits & Slices",
        "Bread Rolls & Buns"
    ],
    }

d10 = {
    "Organic": [
        "Organic & Gluten Free"
    ],
    "Meat": [
        "Frozen Meat"
    ],
    "Vegan & Vegetarian": [
         "Frozen Meat Alternatives"
    ],
    "Fish and Seafood": [
        "Frozen Seafood"
    ],
    "Drinks": [
        "Frozen Fruit & Drink"
    ],
    "Easy Meals": [
        "Frozen Meals & Snacks"
    ],
    "Bakery": [
        "Cakes & Muffins",
        "Fresh Biscuits & Slices",
        "Fresh Breads & Rolls",
        "Fresh Cakes & Muffins",
        "Fresh Desserts & Pastries",
        "Garlic & Herb Breads",
        "Muffin Splits & Crumpets",
        "Pies & Pastries",
        "Sliced Bread",
        "Specialty Breads",
        "Wraps & Pita Breads",
        "Organic & Gluten Free"
    ],
    "Frozen": [
        "Frozen Items",
        "Frozen Desserts",
        "Frozen Fruit & Drink",
        "Frozen Meals & Snacks",
        "Frozen Meat",
        "Frozen Meat Alternatives",
        "Frozen Seafood",
        "Frozen Vegetables"
    ],
    }

d11 = {
    "Fruit and Vegetables": [
        "Frozen Fruit"
    ],
    "Meat": [
        "Frozen Beef Lamb & Pork",
        "Frozen Chicken & Poultry"
    ],
    "Fish and Seafood": ["Frozen Fish"],
    "Easy Meals": [
        "Frozen Dessert Pastries",
        "Frozen Ready Meals",
        "Frozen Pies",
        "Pizza Pastry & Bread"
    ],
    "Bakery": [
        "Frozen Dessert Pastries",
        "Frozen Pastry",
        "Frozen Pies",
        "Baking",
        "Baking Supplies & Sugar",
        "Pizza Pastry & Bread"
    ],
    "Frozen": [
        "Chilled Frozen & Desserts",
        "Frozen Bavarians & Cheesecake",
        "Frozen Fries & Potatoes",
        "Frozen Pizza & Bases",
        "Frozen Savouries",
        "Ice",
        "Ice Cream & Sorbet",
        "Frozen Foods"
    ],
    }

d12 = {
    "Bakery": [
        "Baking Additives",
        "Baking Mixes",
        "Baking Nuts & Seeds",
        "Baking Syrups",
        "Breadcrumbs & Coatings",
        "Cooking Chocolate",
        "Dried Fruit",
        "Essences & Colourings",
        "Flour",
        "Icing & Decorating",
        "Sugar",
        "Sugar Substitutes"
    ],
    "Snacks": [
        "Snacks",
        "Biscuits & Crackers",
        "Assorted Biscuits & Crackers",
        "Biscuits & Cookies",
        "Chocolate Biscuits",
        "Crackers",
        "Crème & Jam Biscuits",
        "Gourmet Biscuits & Crackers"
    ],
    }

d13 = {
    "Fruit and Vegetables": [
        "Fruit Snacks",
        "Vege Snacks"
    ],
    "Meat": [
        "Meat Snacks"
    ],
    "Vegan & Vegetarian": [
        "Rice Cakes",
        "Rice Crackers",
        "Fruit Snacks",
        "Vege Snacks"
    ],
    "Easy Meals": [
        "Breakfast On The Go"
    ],
    "Snacks": [
        "Snack Foods",
        "Snacks & Sweets",
        "Chips",
        "Corn Chips",
        "Meat Snacks",
        "Popcorn",
        "Potato Chips",
        "Snack Mixes",
        "Rice Cakes",
        "Rice Crackers",
        "Fruit Snacks",
        "Vege Snacks",
        "Plain Sweet Biscuits",
        "Bread Snacks",
        "Cereal & Snack Bars",
        "Muesli Bars",
        "Nut Bars & Snacks",
        "Nutritional Bars"
    ],
    }

d14 = {
    "Snacks": [
        "Chewing Gum & Mints",
        "Confectionery",
        "Boxed Chocolates",
        "Chocolate Blocks",
        "Chocolate Family Bags",
        "Lollies Family Bags",
        "Snacks & Sweets",
        "Ready To Serve Puddings",
        "Desserts"
    ],
    "Baking": ["Jelly & Powdered Desserts"],
    "Pantry": [
        "Herbs Spices & Stock",
        "Oil Vinegar & Condiments",
        "Pasta Noodles & Grains",
        "Breakfast Cereals",
        "Gourmet Oils & Condiments",
        "Olives & Antipasti Mixes",
        "Pantry",
        "Specialty Dry Goods"
    ],
    "Other": [
        "Easter eggs and chocolates",
        "Easter feast essentials"
    ]
}

d15 = {
    "Fruit and Vegetables": [
        "Olives",
        "Pickles"
    ],
    "Sauces and Dressings": [
        "Relish",
        "Vinegars"
    ],
    "Butter & Spreads": [
        "Salad & Cooking Oils"
    ],
    "Easy Meals": [
        "Novelty Bars & Singles"
    ],
    "Snacks": [
        "Novelty Bars & Singles"
    ],
    "Pantry": [
        "Pantry",
        "Olives",
        "Pickles",
        "Specialty Grains & Seeds",
        "Hot Cereals",
        "Muesli",
        "Pasta Rice & Noodles",
        "Dried Pastas",
        "Noodles",
        "Specialty Grains & Seeds",
        "Cold Cereals",
        "Flake/Fibre Cereals",
        "Basmati Rices",
        "Jasmine Rices",
        "Long Grain Rices",
        "Short & Medium Grain Rices",
        "Wild & Coloured Rices"
    ]
    }

d16 = {
    "Sauces and Dressings": [
        "Curry Pastes & Sauces",
        "Gravies",
        "Tomato Sauces"
    ],
    "Butter & Spreads": [
        "Avocado Oils",
        "Olive Oils"
    ],
    "International": ["International"],
    "Pantry": [
        "Curry Pastes & Sauces",
        "Gravies",
        "Tomato Pastes & Purees",
        "Tomato Sauces",
        "Avocado Oils",
        "Coconut Oils",
        "Nut & Seed Oils",
        "Oil Sprays",
        "Olive Oils",
        "Other Oils",
        "Rice Bran Oils",
        "Vegetable Oils",
        "Chilli & Paprika",
        "Dried Herbs",
        "Dried Spices",
        "Garlic & Ginger",
        "Salt & Pepper"
    ],
    }

d17 = {
    "Fruit and Vegetables": [
        "Canned & Dried Vegetables",
        "Canned Fruit"
    ],
    "Meat": [
        "Canned Meat"
    ],
    "International": [
        "International",
        "World Foods",
        "Chinese",
        "Indian",
        "Japanese",
        "Korean",
        "Other Countries",
        "South East Asian",
        "Thai",
        "UK",
        "USA"
    ],
    "Fish and Seafood": [
        "Canned Fish"
    ],
    "Dairy and Eggs": [
        "Canned Milk & Cream"
    ],
    "Easy Meals": [
        "Baked Beans & Spaghetti",
        "Canned & Prepared Foods",
        "Tinned Foods"
    ],
    "Pantry": [
        "Canned Desserts",
        "Canned Items",
        "Canned & Dried Vegetables",
        "Canned Fruit",
        "Canned Meat",
        "Canned & Prepared Foods",
        "Tinned Foods",
        "Canned Fish"
    ],
    }
d18 = {
    "Vegan & Vegetarian": [
        "Coconut Cream & Milk"
    ],
    "Personal Care": [
        "Personal Care",
        "Bath Shower & Soap",
        "Contraception & Pregnancy",
        "Dental & Oral Care",
        "Eye & Ear Care",
        "Hair Care",
        "Make Up & Nail Care",
        "Medical & First Aid",
        "Period & Continence Care",
        "Shaving & Hair Removal",
        "Skin Care & Deodorant"
    ],
    "Alcoholic": [
        "Alcohol",
        "Beer",
        "Cider",
        "Red wine",
        "Rose wine",
        "Sparkling & dessert wine",
        "White wine",
        "Liquorice"
    ],
    }

d19 = {
    "Drinks": [
        "Chilled Fruit Juices",
        "Coconut Water",
        "Drinking Yoghurt & Smoothies",
        "Flavoured Water",
        "Fruit Drinks & Juices",
        "Iced Teas"
    ],
    "Kids": [
        "Kids and Babies",
        "Baby Food",
        "Bottles Toys & Accessories",
        "For Mum",
        "Formula",
        "Nappies & Wipes"
    ],
    "Pets": [
        "Birds Fish & Small Animals",
        "Cats",
        "Dogs",
        "Pet health & accessories"
    ],
    "Other": [
        "Easter",
        "Christmas"
    ]
}

d20 = {
    "Fruit and Vegetables": ["Vegetable Juices"],
    "Dairy and Eggs": ["Milk Drink Mixes"],
    "Drinks": ["Powdered Drinks", "Soft Drinks", "Sparkling Juices", "Sparkling Water", "Sports & Energy Drinks",
               "Non Alcoholic", "Vegetable Juices", "Squash Syrups & Cordials", "Milk Drink Mixes", "Still Water"],
    "Alcoholic": ["Beer Cider & Wine", "Beer & Cider Awards", "Cider & Alcoholic Gingerbeer", "IPA", "Lager & Pilsner",
                  "Pale Ale", "Beer & Cider", "American-style Ale", "Apple & Pear Cider", "Craft Beer"],
    }

d21 = {
    "Alcoholic": [
        "Lager",
        "Low & No Alcohol Beers",
        "Specialty & Flavoured Beer",
        "Stout Porter & Black Beer",
        "Wine",
        "Cabernet",
        "Cask Wine",
        "Champagne & Sparkling Wine",
        "Chardonnay",
        "Low & No Alcohol Wines",
        "Merlot",
        "Other Red Wine",
        "Other White Wine",
        "Pinot Gris",
        "Pinot Noir",
        "Rose",
        "Fruit & Flavoured Cider",
        "Seltzer",
        "Low & No Alcohol Beers",
        "Mixers"
    ],
    }

d22 = {
    "Personal Care": [
        "Personal Care",
        "Beauty & Grooming",
        "Deodorants",
        "Face & Lip Skin Care",
        "Hair Care & Treatments",
        "Hair Colouring",
        "Hair Styling & Accessories",
        "Hand & Body Care",
        "Makeup & Cosmetics",
        "Oral Health",
        "Shaving & Hair Removal",
        "Suncare & Self Tan",
        "Health & Wellness",
        "Adult Care",
        "Allergy & Sinus",
        "Cough Cold & Flu",
        "Digestion Nausea & Laxatives"
    ],
    "Alcoholic": ["Shiraz", "Sauvignon Blanc"],
    }

d23 = {
    "Kids": ["Baby Toddler & Kids", "Baby Care", "Baby Bathing & Skin Care", "Baby Dental Care",
             "Baby Formula & Toddler Food", "Baby Hair Care", "Baby Health", "Baby Wipes", "Nappies & Changing",
             "Nursing & Feeding"],
    "Pets": ["Pets", "Pet Supplies"],
    "Personal Care": ["Family Planning", "First Aid", "Pain Relief", "Sanitary Protection",
                      "Stop Smoking", "Vitamins & Supplements", "Wellness & Sports Nutrition"],
    "Other": ["Insect Repellent"]
}

d24 = {
    "Pets": [
        "Cat Accessories",
        "Cat Food",
        "Dog Food",
        "Dog Treats"
    ],
    "Cleaning, Laundry And Bathroom": [
        "Cleaning Products",
        "All Purpose Cleaners",
        "Bathroom & Shower Cleaners",
        "Bleaches",
        "Carpet & Floor Cleaners",
        "Cleaning Accessories",
        "Dishwasher Detergents",
        "Dishwasher Rinse & Clean",
        "Dishwashing Liquid",
        "Furniture & Metal Polishes",
        "Glass Cleaners",
        "Kitchen Cleaners",
        "Paper Towels",
        "Brushes"
    ],
    "Other": ["Garage & Outdoor"]
}

d25 = {
    "Cleaning, Laundry And Bathroom": [
        "Glue & Adhesives",
        "Air Fresheners & Deodorisers",
        "Household",
        "Disposable Tableware",
        "Pest & Insect Control",
        "Rubbish & Vacuum Bags"
    ],
    "Baking": [
        "Cooking & Bakeware",
        "Food Storage",
        "Food Wraps & Bags",
        "Kitchenware"
    ],
    "Other": [
        "Light Bulbs",
        "Hooks",
        "Tape",
        "Electrical",
        "Fire Needs",
        "Homeware",
        "Manchester",
        "Party Supplies"
    ]
}

d26 = {
    "Fruit and Vegetables": [
        "Fresh Salads",
        "Vege Bags"
    ],
    "Meat": [
        "PrePacked Pork"
    ],
    "Fish and Seafood": [
        "Fresh Fish Heads",
        "Fresh Whole Fish"
    ],
    "Deli": [
        "Deli Cabinet Cheeses"
    ],
    "Bakery": [
        "Dessert Pastries"
    ],
    "Cleaning, Laundry And Bathroom": [
        "Tissues & Toilet Paper",
        "Laundry",
        "Fabric Softeners",
        "Laundry Liquid & Capsules",
        "Laundry Powders",
        "Laundry Supplies",
        "Pre Wash Stain Removers"
    ],
    "Snacks": [
        "Gourmet Confectionery"
    ],
    "Kids": ["Toys & Recreation"],
    "Other": [
        "Stationery & Entertainment",
        "Newspapers",
        "Stationery & Craft",
        "Tobacco Papers & Filters"
    ]
}

d27 = {
    "Fruit and Vegetables": ["Freshly Ground Herbs"],
    "Sauces and Dressings": [
        "Tartare & Seafood Sauces"
    ],
    "Drinks": [
        "Coffee Substitutes",
        "Brewing Supplies"   
    ],
    "Bakery": [
        "Frozen Bread & Dough"
    ],
    "Pets": [
        "Bird Supplies",
        "Cat Treats",
        "Dog Accessories",
        "Pet Accessories",
        "Pet Treatments",
        "Small Animal Supplies",
        "Fish & Aquatic Pet Supplies"
    ],
    "Personal Care": [
        "Foot Care"
    ],
    "Frozen": [
        "Frozen Puddings"
    ],
    "Alcoholic": [
        "British-style Ale",
        "European-style Ale",
        "Sake"
    ],
    "Pantry": [
        "Cooking Fat"
    ],
    "Other": [
        "BBQ"
    ]
}
d28 = {
    "Cleaning, Laundry And Bathroom": ["Car Care", "Shoe Care", "Fine Fabric Washers", "Laundry Soap", "Washing Machine Cleaners"],
    "Other": ["Gardening Supplies", "Clothes Pegs", "Magazines"]
}

d29 = {
    "Cleaning, Laundry And Bathroom": ["Tissues & Cotton Buds", "Cleaning", "Laundry", "Bags", "Bathroom"],
    "Personal Care": ["Vitamins & Nutrition", "Sports & Fitness"],
    "Other": ["Other",
              "Clothing & Accessories", "Entertainment & Gifts", "Garden & Garage", "Homewares",
              "Hardware & Electrical", "Kitchen", "Restricted Items", "Featured", "Pest Control", "Magazines & Stationery"]
}

d30 = {
    "Easy Meals": ["Pasta Pizza & Pastry", "Prepared Meals & Sides", "Meal Kits", "Meal Spot", "Ready to Cook",
                   "Mexican", "Noodle Meals", "Pasta Meals", "Simply DINNER", "Ready to Eat", "Ready to Heat",
                   "Canned Soup", "Chilled Pies & Pastries", "Chilled Soups", "Packet Soup", "Pizza & Pizza Bases",
                   "Ready Meals"],
    "Snacks": ["Chilled Custards", "Ice Blocks & Ice Pops"],
    "Frozen": ["Ice Cream & Frozen Yoghurt"],
    }

keys = [
    "International", "Fruit and Vegetables", "Organic", "Meat", "Vegan & Vegetarian",
    "Sauces and Dressings", "Sauces and Dressings", "Bulk Buys", "Fish and Seafood",
    "Butter & Spreads", "Dairy and Eggs", "Deli", "Drinks", "Easy Meals", "Bakery",
    "Kids", "Pets", "Cleaning, Laundry And Bathroom", "Personal Care", "Snacks", "Baking", "Frozen", "Alcoholic",
    "Pantry", "Other"
]

dicts = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22, d23, d24,
         d25, d26, d27, d28, d29, d30]

outFile = open("finalCategories.json", mode="w")
outFile.write("{")
finaldict = {str: [str]}
for key in keys:
    finaldict[key] = []
    for dict in dicts:
        if key in dict:
            for item in dict[key]:
                if item not in finaldict[key]:
                    finaldict[key].append(item)

for key in keys:
    print(key)
    outFile.write(f'"{str(key)}": [ \n')
    for item in finaldict[key]:
        outFile.write(f'    "{item}"' + ",\n")
    outFile.write("],\n")

outFile.write("}\n")
outFile.close()