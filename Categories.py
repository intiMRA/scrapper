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
    "Organic": ["Organic", "Organic"],
    "Meat": ["Meat", "BBQ Meat", "Beef", "Chicken & Poultry"],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": ["Shop Fresh Deals"]
}

d2 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": ["Lamb", "Mince & Patties", "Offal & Bones", "Pork", "Roast Meat", "Sausages", "Venison & Game", "Butchery",
             "Fresh Beef & Lamb", "Fresh Chicken & Poultry", "Fresh Pork", "Fresh Sausages",
             "Fresh Venison & Game Meat", "PreCooked Sausages", "PrePacked Beef & Lamb", "PrePacked Chicken & Poultry",
             "PrePacked Sausages", "Bacon", "Continental Sausage & Salami", "Ham & Pork"],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d3 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [
        "PreCooked Beef & Lamb",
        "PreCooked Chicken & Poultry"
    ],
    "Vegan & Vegetarian": [
        "Vegan & Vegetarian",
        "Vegan & Vegetarian",
        "Vegan",
        "Pams Plant Based",
        "Vegan range",
        "Meat Free",
        "Frozen Vegetarian",
        "Vegetarian"
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
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [
        "Dairy & Lactose Free"
    ],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": [
        "Plant based alternatives"
    ]
}

d4 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
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
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d5 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
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
        "Butter & Spreads"
    ],
    "Dairy and Eggs": [],
    "Deli": [
        "Dips Hummus & Nibbles",
        "Dips Pesto & Pate"
    ],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [
        "Frozen Fish & Seafood"
    ],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d6 = {
    "Fruit and Vegetables": [],
    "Organic": [
        "Fresh Organic Milk"
    ],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [
        "Dips & Salsas"
    ],
    "Bulk Buys": [],
    "Fish and Seafood": [],
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
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d7 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
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
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}
d8 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": ["Low & no alcohol", "Coffee", "Juice & Cordial", "Soft Drinks & Sports Drinks", "Tea & Milk Drinks",
               "Water", "Cold Drinks", "Hot Drinks", "Black Teas", "Chai Teas", "Chocolate Milk Drink Mixes",
               "Coffee Additives & Filters", "Coffee Capsules", "Coffee Flavoured Sachets", "Fresh Coffees",
               "Fruit & Herbal Teas", "Green Teas", "Instant Coffees", "Malt Milk Drink Mixes"],
    "Easy Meals": ["Easy Meals"],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d9 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [
        "Ice Cream Cones & Wafers",
        "Fresh Pastas",
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
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": ["Instant Rices", "Rice Meals"]
}

d10 = {
    "Fruit and Vegetables": [],
    "Organic": [
        "Organic & Gluten Free"
    ],
    "Meat": [
        "Frozen Meat",
        "Frozen Meat Alternatives"
    ],
    "Vegan & Vegetarian": [
        "Organic & Gluten Free"
    ],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [
        "Frozen Seafood"
    ],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
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
        "Wraps & Pita Breads"
    ],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
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
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d11 = {
    "Fruit and Vegetables": [
        "Frozen Fruit"
    ],
    "Meat": [
        "Frozen Beef Lamb & Pork",
        "Frozen Chicken & Poultry",
        "Frozen Fish"
    ],
    "Vegan & Vegetarian": [
        "Pizza Pastry & Bread"
    ],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [
        "Frozen Ready Meals"
    ],
    "Bakery": [
        "Frozen Dessert Pastries",
        "Frozen Foods",
        "Frozen Pastry",
        "Frozen Pies",
        "Baking",
        "Baking",
        "Baking Supplies & Sugar"
    ],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Frozen": [
        "Chilled Frozen & Desserts",
        "Frozen Bavarians & Cheesecake",
        "Frozen Fries & Potatoes",
        "Frozen Pizza & Bases",
        "Frozen Savouries",
        "Ice",
        "Ice Cream & Sorbet"
    ],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d12 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
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
        "Sugar Substitutes",
        "Assorted Biscuits & Crackers",
        "Biscuits & Cookies",
        "Chocolate Biscuits",
        "Crackers",
        "Crème & Jam Biscuits",
        "Gourmet Biscuits & Crackers"
    ],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [
        "Snacks",
        "Biscuits & Crackers"
    ],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d13 = {
    "Fruit and Vegetables": [
        "Fruit Snacks",
        "Vege Snacks"
    ],
    "Organic": [],
    "Meat": [
        "Meat Snacks"
    ],
    "Vegan & Vegetarian": [
        "Rice Cakes",
        "Rice Crackers",
        "Fruit Snacks",
        "Vege Snacks"
    ],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [
        "Breakfast On The Go"
    ],
    "Bakery": [
        "Plain Sweet Biscuits",
        "Bread Snacks",
        "Cereal & Snack Bars",
        "Muesli Bars",
        "Nut Bars & Snacks",
        "Nutritional Bars",
        "Something Sweet"
    ],
    "Kids": [
        "Breakfast On The Go",
        "Fruit Snacks",
        "Something Sweet"
    ],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [
        "Snack Foods",
        "Snacks & Sweets",
        "Chips",
        "Corn Chips",
        "Meat Snacks",
        "Popcorn",
        "Potato Chips",
        "Snack Mixes",
        "Something Sweet"
    ],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d14 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [
        "Chewing Gum & Mints",
        "Confectionery",
        "Boxed Chocolates",
        "Chocolate Blocks",
        "Chocolate Family Bags",
        "Lollies Family Bags",
        "Snacks & Sweets"
    ],
    "Baking": [
        "Jelly & Powdered Desserts"
    ],
    "Frozen": [
        "Easter eggs and chocolates",
        "Ready To Serve Puddings",
        "Specialty Dry Goods"
    ],
    "Alcoholic": [],
    "Pantry": [
        "Desserts",
        "Easter feast essentials",
        "Herbs Spices & Stock",
        "Oil Vinegar & Condiments",
        "Pasta Noodles & Grains",
        "Breakfast Cereals",
        "Gourmet Oils & Condiments",
        "Olives & Antipasti Mixes",
        "Pantry"
    ],
    "Other": []
}

d15 = {
    "Fruit and Vegetables": [
        "Olives",
        "Pickles"
    ],
    "Organic": [
        "Specialty Grains & Seeds"
    ],
    "Meat": [],
    "Vegan & Vegetarian": [
        "Hot Cereals",
        "Muesli",
        "Pasta Rice & Noodles",
        "Dried Pastas",
        "Noodles",
        "Specialty Grains & Seeds"
    ],
    "Sauces and Dressings": [
        "Relish",
        "Vinegars"
    ],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [
        "Salad & Cooking Oils"
    ],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [
        "Novelty Bars & Singles"
    ],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [
        "Pantry",
        "Cold Cereals",
        "Flake/Fibre Cereals"
    ],
    "Baking": [],
    "Frozen": [
        "Basmati Rices",
        "Jasmine Rices",
        "Long Grain Rices",
        "Short & Medium Grain Rices",
        "Wild & Coloured Rices"
    ],
    "Alcoholic": [],
    "Pantry": [
        "Pantry"
    ],
    "Other": []
}

d16 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [
        "Curry Pastes & Sauces",
        "Gravies",
        "Tomato Pastes & Purees",
        "Tomato Sauces"
    ],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [
        "Avocado Oils",
        "Coconut Oils",
        "Nut & Seed Oils",
        "Oil Sprays",
        "Olive Oils",
        "Other Oils",
        "Rice Bran Oils",
        "Vegetable Oils"
    ],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [
        "Chilli & Paprika",
        "Dried Herbs",
        "Dried Spices",
        "Garlic & Ginger",
        "Salt & Pepper"
    ],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [
        "International"
    ],
    "Other": []
}

d17 = {
    "Fruit and Vegetables": [
        "Canned & Dried Vegetables",
        "Canned Fruit"
    ],
    "Meat": [
        "Canned Meat"
    ],
    "Vegan & Vegetarian": [
        "World Foods",
        "Chinese",
        "Indian",
        "Japanese",
        "Korean",
        "Other Countries",
        "South East Asian",
        "Thai"
    ],
    "Sauces and Dressings": [
        "Canned & Prepared Foods"
    ],
    "Bulk Buys": [
        "Tinned Foods"
    ],
    "Fish and Seafood": [
        "Canned Fish"
    ],
    "Butter & Spreads": [
        "Canned Milk & Cream"
    ],
    "Dairy and Eggs": [
        "UK"
    ],
    "Drinks": [
        "USA"
    ],
    "Easy Meals": [
        "Baked Beans & Spaghetti",
        "Canned Desserts"
    ],
    "Bakery": [

    ],
    "Kids": [

    ],
    "Pets": [

    ],
    "Cleaning": [

    ],
    "Personal Care": [

    ],
    "Snacks": [

    ],
    "Baking": [

    ],
    "Frozen": [

    ],
    "Alcoholic": [

    ],
    "Pantry": [
        "Canned Items"
    ],
    "Other": [

    ]
}
d18 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [
        "Coconut Cream & Milk",
        "Beer",
        "Cider",
        "Red wine",
        "Rose wine",
        "Sparkling & dessert wine",
        "White wine",
        "Liquorice",
        "Alcohol"
    ],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
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
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
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
    "Pantry": [],
    "Other": []
}

d19 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [
        "Chilled Fruit Juices",
        "Coconut Water",
        "Drinking Yoghurt & Smoothies",
        "Flavoured Water",
        "Fruit Drinks & Juices",
        "Iced Teas"
    ],
    "Easy Meals": [],
    "Bakery": [],
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
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": [
        "Easter",
        "Christmas"
    ]
}

d20 = {
    "Fruit and Vegetables": ["Vegetable Juices"],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": ["Squash Syrups & Cordials"],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": ["Milk Drink Mixes", "Still Water"],
    "Deli": [],
    "Drinks": ["Powdered Drinks", "Soft Drinks", "Sparkling Juices", "Sparkling Water", "Sports & Energy Drinks",
               "Beer Cider & Wine", "Beer & Cider Awards", "Cider & Alcoholic Gingerbeer", "IPA", "Lager & Pilsner",
               "Non Alcoholic", "Pale Ale", "Beer & Cider", "American-style Ale", "Apple & Pear Cider", "Craft Beer"],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": ["Beer Cider & Wine", "Beer & Cider Awards", "Cider & Alcoholic Gingerbeer", "IPA", "Lager & Pilsner",
                  "Pale Ale", "Beer & Cider", "American-style Ale", "Apple & Pear Cider", "Craft Beer"],
    "Pantry": [],
    "Other": []
}

d21 = {
    "Fruit and Vegetables": [
        "Fruit & Flavoured Cider",
        "Seltzer"
    ],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [
        "Low & No Alcohol Beers"
    ],
    "Sauces and Dressings": [
        "Mixers"
    ],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [
        "Lager",
        "Pilsner",
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
        "Rose"
    ],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
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
        "Rose"
    ],
    "Pantry": [],
    "Other": []
}

d22 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": ["Sauvignon Blanc"],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
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
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": ["Shiraz"],
    "Pantry": [],
    "Other": []
}

d23 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": ["Baby Toddler & Kids", "Baby Care", "Baby Bathing & Skin Care", "Baby Dental Care",
             "Baby Formula & Toddler Food", "Baby Hair Care", "Baby Health", "Baby Wipes", "Nappies & Changing",
             "Nursing & Feeding"],
    "Pets": ["Pets", "Pet Supplies"],
    "Cleaning": [],
    "Personal Care": ["Family Planning", "First Aid", "Insect Repellent", "Pain Relief", "Sanitary Protection",
                      "Stop Smoking", "Vitamins & Supplements", "Wellness & Sports Nutrition"],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d24 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [
        "Cat Accessories",
        "Cat Food",
        "Dog Food",
        "Dog Treats"
    ],
    "Cleaning": [
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
        "Garage & Outdoor",
        "Brushes"
    ],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

d25 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [
        "Glue & Adhesives",
        "Air Fresheners & Deodorisers",
        "Household",
        "Disposable Tableware",
        "Pest & Insect Control",
        "Rubbish & Vacuum Bags"
    ],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [
        "Cooking & Bakeware",
        "Food Storage",
        "Food Wraps & Bags",
        "Kitchenware",
        "Light Bulbs"
    ],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": [
        "Hooks",
        "Tape",
        "Electrical",
        "Fire Needs",
        "Homeware",
        "Manchester",
        "Party Supplies"
    ],
    "Other": []
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
    "Cleaning": [
        "Tissues & Toilet Paper",
        "Laundry",
        "Fabric Softeners",
        "Laundry Liquid & Capsules",
        "Laundry Powders",
        "Laundry Supplies",
        "Pre Wash Stain Removers"
    ],
    "Personal Care": [
        "Stationery & Entertainment",
        "Newspapers",
        "Stationery & Craft",
        "Tobacco Papers & Filters"
    ],
    "Snacks": [
        "vGourmet Confectionery"
    ],
    "Other": [
        "Toys & Recreation"
    ]
}

d27 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [
        "Tartare & Seafood Sauces"
    ],
    "Bulk Buys": [],
    "Fish and Seafood": [
        "Fish & Aquatic Pet Supplies"
    ],
    "Butter & Spreads": [],
    "Dairy and Eggs": [
        "Freshly Ground Herbs"
    ],
    "Deli": [],
    "Drinks": [
        "Coffee Substitutes",
        "Brewing Supplies",
        "Sake"
    ],
    "Easy Meals": [],
    "Bakery": [
        "Frozen Bread & Dough"
    ],
    "Kids": [],
    "Pets": [
        "Bird Supplies",
        "Cat Treats",
        "Dog Accessories",
        "Pet Accessories",
        "Pet Treatments",
        "Small Animal Supplies"
    ],
    "Cleaning": [],
    "Personal Care": [
        "Foot Care"
    ],
    "Snacks": [],
    "Baking": [],
    "Frozen": [
        "Frozen Puddings"
    ],
    "Alcoholic": [
        "British-style Ale",
        "European-style Ale"
    ],
    "Pantry": [
        "Cooking Fat"
    ],
    "Other": [
        "BBQ"
    ]
}
d28 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": ["Car Care", "Shoe Care", "Fine Fabric Washers", "Laundry Soap", "Washing Machine Cleaners"],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": ["Magazines"],
    "Other": ["Gardening Supplies", "Clothes Pegs"]
}

d29 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": [],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": ["Tissues & Cotton Buds", "Cleaning", "Laundry", "Pest Control"],
    "Personal Care": [],
    "Snacks": [],
    "Baking": [],
    "Frozen": [],
    "Alcoholic": [],
    "Pantry": ["Magazines & Stationery"],
    "Other": ["Sports & Fitness", "Sports & Fitness", "Vitamins & Nutrition", "Bags", "Bathroom", "Other",
              "Clothing & Accessories", "Entertainment & Gifts", "Garden & Garage", "Homewares",
              "Hardware & Electrical", "Kitchen", "Restricted Items", "Featured"]
}

d30 = {
    "Fruit and Vegetables": [],
    "Organic": [],
    "Meat": [],
    "Vegan & Vegetarian": [],
    "Sauces and Dressings": [],
    "Bulk Buys": [],
    "Fish and Seafood": [],
    "Butter & Spreads": [],
    "Dairy and Eggs": [],
    "Deli": [],
    "Drinks": [],
    "Easy Meals": ["Pasta Pizza & Pastry", "Prepared Meals & Sides", "Meal Kits", "Meal Spot", "Ready to Cook",
                   "Mexican", "Noodle Meals", "Pasta Meals", "Simply DINNER", "Ready to Eat", "Ready to Heat",
                   "Canned Soup", "Chilled Pies & Pastries", "Chilled Soups", "Packet Soup", "Pizza & Pizza Bases",
                   "Ready Meals"],
    "Bakery": [],
    "Kids": [],
    "Pets": [],
    "Cleaning": [],
    "Personal Care": [],
    "Snacks": ["Chilled Custards", "Ice Blocks & Ice Pops"],
    "Baking": [],
    "Frozen": ["Ice Cream & Frozen Yoghurt"],
    "Alcoholic": [],
    "Pantry": [],
    "Other": []
}

dicts = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22, d23, d24,
         d25, d26, d27, d28, d29, d30]
