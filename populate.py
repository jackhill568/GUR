import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "GUR.settings")
import django
django.setup()


from main.helpers import *
import random

FIRST_NAMES = [
    "James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","William","Elizabeth",
    "David","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Charles","Karen",
    "Christopher","Nancy","Daniel","Lisa","Matthew","Betty","Anthony","Margaret","Mark","Sandra",
    "Donald","Ashley","Steven","Kimberly","Paul","Emily","Andrew","Donna","Joshua","Michelle",
    "Kenneth","Dorothy","Kevin","Carol","Brian","Amanda","George","Melissa","Edward","Deborah",
    "Ronald","Stephanie","Timothy","Rebecca","Jason","Sharon","Jeffrey","Laura","Ryan","Cynthia",
    "Jacob","Kathleen","Gary","Amy","Nicholas","Angela","Eric","Shirley","Jonathan","Anna",
    "Stephen","Brenda","Larry","Pamela","Justin","Emma","Scott","Nicole","Brandon","Helen",
    "Benjamin","Samantha","Samuel","Katherine","Frank","Christine","Gregory","Debra","Raymond","Rachel",
    "Alexander","Catherine","Patrick","Carolyn","Jack","Janet","Dennis","Ruth","Jerry","Maria",
    "Tyler","Heather","Aaron","Diane","Jose","Virginia","Henry","Julie","Adam","Joyce",
    "Douglas","Victoria","Nathan","Olivia","Peter","Kelly","Zachary","Christina","Kyle","Lauren",
    "Walter","Joan","Harold","Evelyn","Jeremy","Judith","Ethan","Megan","Carl","Cheryl",
    "Keith","Andrea","Roger","Hannah","Gerald","Martha","Christian","Jacqueline","Terry","Frances",
    "Sean","Gloria","Arthur","Ann","Austin","Teresa","Noah","Kathryn","Lawrence","Sara",
    "Jesse","Janice","Joe","Jean","Bryan","Alice","Billy","Madison","Jordan","Doris",
    "Albert","Abigail","Dylan","Julia","Bruce","Judy","Willie","Grace","Gabriel","Denise",
    "Alan","Amber","Juan","Marilyn","Logan","Beverly","Wayne","Danielle","Ralph","Theresa",
    "Roy","Sophia","Eugene","Marie","Randy","Diana","Vincent","Brittany","Russell","Natalie",
    "Elijah","Isabella","Louis","Charlotte","Bobby","Rose","Philip","Alexis","Johnny","Kayla"
]
LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
    "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
    "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
    "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts",
    "Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes",
    "Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper",
    "Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson",
    "Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes",
    "Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez",
    "Powell","Jenkins","Perry","Russell","Sullivan","Bell","Coleman","Butler","Henderson","Barnes",
    "Gonzales","Fisher","Vasquez","Simmons","Romero","Jordan","Patterson","Alexander","Hamilton","Graham",
    "Reynolds","Griffin","Wallace","Moreno","West","Cole","Hayes","Bryant","Herrera","Gibson",
    "Ellis","Tran","Medina","Aguilar","Stevens","Murray","Ford","Castro","Marshall","Owens",
    "Harrison","Fernandez","Mcdonald","Woods","Washington","Kennedy","Wells","Vargas","Henry","Chen",
    "Freeman","Webb","Tucker","Guzman","Burns","Crawford","Olson","Simpson","Porter","Hunter",
    "Gordon","Mendez","Silva","Shaw","Snyder","Mason","Dixon","Munoz","Hunt","Hicks",
    "Holmes","Palmer","Wagner","Black","Robertson","Boyd","Rose","Stone","Salazar","Fox",
    "Warren","Mills","Meyer","Rice","Schmidt","Garza","Daniels","Ferguson","Nichols","Stephens"
]
def generate_mass_users(n):
    users = []
    for i in range(n):
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)

        users.append({
            "first_name": fn,
            "last_name": ln,
            "email": f"{fn.lower()}{ln.lower()}{i}@mail.com",
            "nickname": f"{fn.lower()}{i}",
            "password": "pass123",
            "profile_picture": "",
            "score": random.randint(0, 2000),
            "permission_level": random.choice([1, 2, 2, 2, 2]) 
        })
    return users

USER_DATA = generate_mass_users(1000)

INGREDIENTS = [
    "Salt","Black Pepper","White Pepper","Sugar","Brown Sugar","Flour","Bread Flour","Baking Powder","Baking Soda","Yeast",
    "Cornstarch","Vanilla Extract","Honey","Maple Syrup","Olive Oil","Vegetable Oil","Butter","Margarine","Milk","Cream",
    "Chicken Breast","Chicken Thigh","Ground Beef","Beef Steak","Pork Chop","Bacon","Sausage","Turkey","Duck","Lamb",
    "Salmon","Tuna","Cod","Shrimp","Prawns","Crab","Lobster","Eggs","Tofu","Tempeh",
    "Onion","Red Onion","Garlic","Ginger","Carrot","Potato","Sweet Potato","Tomato","Cherry Tomato","Cucumber",
    "Bell Pepper","Red Bell Pepper","Green Bell Pepper","Yellow Bell Pepper","Zucchini","Eggplant","Broccoli","Cauliflower",
    "Spinach","Kale","Lettuce","Cabbage","Mushroom","Green Beans","Peas","Corn","Asparagus","Leek","Radish",
    "Apple","Banana","Orange","Lemon","Lime","Strawberry","Blueberry","Raspberry","Blackberry","Pineapple",
    "Mango","Papaya","Kiwi","Grapes","Watermelon","Peach","Pear","Plum","Coconut","Avocado",
    "Basil","Parsley","Cilantro","Mint","Rosemary","Thyme","Oregano","Dill","Chives","Sage",
    "Cumin","Turmeric","Paprika","Smoked Paprika","Chili Powder","Cayenne Pepper","Cinnamon","Nutmeg","Cloves","Cardamom",
    "Mustard Seeds","Fennel Seeds","Coriander","Bay Leaves","Star Anise","Saffron",
    "Rice","Brown Rice","Jasmine Rice","Basmati Rice","Pasta","Spaghetti","Fusilli","Noodles","Quinoa","Barley",
    "Oats","Bread","Whole Wheat Bread","Tortilla","Wrap","Couscous",
    "Cheddar Cheese","Mozzarella","Parmesan","Feta Cheese","Goat Cheese","Cream Cheese","Yogurt","Greek Yogurt",
    "Condensed Milk","Evaporated Milk",
    "Soy Sauce","Fish Sauce","Oyster Sauce","Tomato Sauce","Ketchup","Mayonnaise","Mustard","Hot Sauce",
    "BBQ Sauce","Vinegar","Apple Cider Vinegar","Balsamic Vinegar","Sesame Oil","Teriyaki Sauce",
    "Almonds","Peanuts","Cashews","Walnuts","Hazelnuts","Pistachios","Chia Seeds","Flax Seeds","Sunflower Seeds","Pumpkin Seeds",
    "Chocolate","Dark Chocolate","Milk Chocolate","Cocoa Powder","White Chocolate","Sprinkles","Food Coloring",
    "Gelatin","Marshmallows",
    "Paneer","Chickpeas","Lentils","Black Beans","Kidney Beans","Hummus","Pita Bread","Curry Paste",
    "Kimchi","Miso Paste","Seaweed","Wasabi","Sriracha","Tahini","Harissa",
    "Coffee","Tea","Green Tea","Black Tea","Orange Juice","Apple Juice","Coconut Milk","Almond Milk","Soy Milk"
]
INGREDIENT_DATA = [{"name": i} for i in INGREDIENTS]


CATEGORIES = [
    "Italian","Mexican","Indian","Chinese","Japanese","Thai","French","Spanish","Greek","Turkish",
    "American","British","Korean","Vietnamese","Mediterranean","Middle Eastern","Caribbean","African","German","Brazilian",

    "Breakfast","Brunch","Lunch","Dinner","Snack","Dessert","Appetizer","Side Dish","Main Course","Street Food",

    "Vegan","Vegetarian","Gluten Free","Dairy Free","Low Carb","Keto","Paleo","High Protein","Low Fat","Sugar Free",

    "Grilled","Baked","Fried","Roasted","Steamed","Boiled","Slow Cooked","Pressure Cooked","Stir Fry","Air Fried",
    "Easy","Medium","Hard","Beginner Friendly","Quick Meals","30 Minute Meals","One Pot","Minimal Ingredients",

    "Chicken","Beef","Pork","Seafood","Fish","Vegetables","Pasta","Rice","Noodles","Cheese",
    "Egg Based","Tofu","Legumes","Beans","Lentils",

    "Holiday","Christmas","Thanksgiving","Easter","Party","BBQ","Picnic","Date Night","Comfort Food","Family Friendly",

    "Healthy","Weight Loss","Muscle Gain","Low Sodium","Heart Healthy","Diabetic Friendly","Clean Eating",

    "Tex Mex","Sichuan","Cantonese","Punjabi","Southern US","New England","Californian","Andalusian",

    "Soup","Salad","Sandwich","Burger","Pizza","Pasta Dish","Curry","Stew","Casserole","Wrap",
    "Tacos","Sushi","Dumplings","Pie","Cake","Cookies","Ice Cream",

    "Smoothies","Juices","Cocktails","Mocktails","Hot Drinks","Cold Drinks",

    "Fusion","Street Style","Gourmet","Fine Dining","Homemade","Budget Meals","Meal Prep","Batch Cooking"
]

CATEGORY_DATA = [{"name": c} for c in CATEGORIES]


def generate_recipes_with_existing_data(n=500, categories_data=None, ingredients_data=None):
    """
    Generates recipes using existing CATEGORY_DICTS and INGREDIENT_DICTS.
    
    Returns:
    - recipes: list of recipe dictionaries for add_recipe()
    - recipe_ingredients: list of recipe-ingredient mappings for add_recipe_ingredients()
    """
    if categories_data is None or ingredients_data is None:
        raise ValueError("You must provide categories_data and ingredients_data")

    category_names = [c["name"] for c in categories_data]
    ingredient_names = [i["name"] for i in ingredients_data]

    recipes = []
    recipe_ingredients = []

    for i in range(1, n + 1):
        main_ingredient = random.choice(ingredient_names)
        name = f"{random.choice(['Delicious','Tasty','Classic','Spicy','Sweet','Savory'])} {main_ingredient} Recipe {i}"

        picture = f"recipes/default.jpg"

        description = f"A {random.choice(['delicious','tasty','quick','easy','healthy','classic'])} recipe using {main_ingredient}."
        method = f"Cook {random.randint(3,8)} ingredients step by step to make {name}."

        recipe_categories = random.sample(category_names, k=min(3, len(category_names)))

        recipes.append({
            "name": name,
            "picture": picture,
            "description": description,
            "method": method,
            "categories": recipe_categories
        })

        num_ingredients = random.randint(3,10)
        selected_ingredients = random.sample(ingredient_names, k=min(num_ingredients, len(ingredient_names)))

        for ing in selected_ingredients:
            recipe_ingredients.append({
                "ingredient": ing,
                "recipe": name,
                "quantity": str(random.randint(50, 500)),
                "unit": random.choice(["g","ml","pcs","tbsp","tsp"])
            })

    return recipes, recipe_ingredients


def generate_reviews(users_data, recipes_data, n_reviews=5000):
 
    if not users_data or not recipes_data:
        raise ValueError("users_data and recipes_data must be provided")

    reviews = []

    review_descriptions = [
        "Amazing recipe, will cook again!",
        "Pretty good, but could be better.",
        "Loved it! My family enjoyed it.",
        "Too spicy for my taste.",
        "Perfect for quick meals.",
        "Easy to follow and delicious.",
        "Not bad, but needs more seasoning.",
        "Absolutely fantastic!",
        "Average taste, nothing special.",
        "Super healthy and tasty!"
    ]

    for _ in range(n_reviews):
        user = random.choice(users_data)
        recipe = random.choice(recipes_data)

        review = {
            "user": user["nickname"],
            "recipe": recipe["name"],
            "description": random.choice(review_descriptions),
            "rating": random.randint(1, 5)
        }

        reviews.append(review)

    return reviews


RECIPE_DATA, RECIPE_INGREDIENT_DATA = generate_recipes_with_existing_data(500, CATEGORY_DATA, INGREDIENT_DATA)

REVIEW_DATA = generate_reviews(USER_DATA, RECIPE_DATA, 5000)



def populate():
    
    print("adding ingredients")
    for data in INGREDIENT_DATA:
        add_ingredient(data["name"])

    print("adding categories")
    for data in CATEGORY_DATA:
        add_category(data["name"])

    print("adding users")
    for data in USER_DATA:
        add_user(data)

    print("adding recipes")
    for data in RECIPE_DATA:
        add_recipe(data)

    print("adding recipe/ingredient mapping")
    for data in RECIPE_INGREDIENT_DATA:
        add_recipe_ingredients(data)


    print("adding reviews")
    for data in REVIEW_DATA:
        add_review(data)


if __name__ == '__main__':
    print("starting population... ")
    populate()
    print("population complete")




