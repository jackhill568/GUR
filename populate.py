import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "GUR.settings")
import django
django.setup()


from main.helpers import *

USER_DATA = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "nickname": "jdoe",
        "email": "jdoe@example.com",
        "password": "",
        "profile_picture": "profile_pics/jdoe.jpg",
        "score": 150,
        "permission_level": 2,
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "nickname": "jsmith",
        "email": "jsmith@example.com",
        "password": "",
        "profile_picture": "profile_pics/jsmith.jpg",
        "score": 320,
        "permission_level": 1,
    },
    {
        "first_name": "Michael",
        "last_name": "Brown",
        "nickname": "mbrown",
        "email": "mbrown@example.com",
        "password": "",
        "profile_picture": "profile_pics/mbrown.jpg",
        "score": 75,
        "permission_level": 2,
    },
    {
        "first_name": "Emily",
        "last_name": "Davis",
        "nickname": "emilyd",
        "email": "emilyd@example.com",
        "password": "",
        "profile_picture": "profile_pics/emilyd.jpg",
        "score": 210,
        "permission_level": 2,
    },
    {
        "first_name": "Admin",
        "last_name": "User",
        "nickname": "superadmin",
        "email": "admin@example.com",
        "password": "",
        "profile_picture": "profile_pics/admin.jpg",
        "score": 999,
        "permission_level": 1,
    },
]

INGREDIENT_DATA = [
    {"name": "Tomato"},
    {"name": "Onion"},
    {"name": "Garlic"},
    {"name": "Chicken Breast"},
    {"name": "Ground Beef"},
    {"name": "Olive Oil"},
    {"name": "Salt"},
    {"name": "Black Pepper"},
    {"name": "Basil"},
    {"name": "Oregano"},
    {"name": "Milk"},
    {"name": "Butter"},
    {"name": "Eggs"},
    {"name": "Flour"},
    {"name": "Sugar"},
]

CATEGORY_DATA = [
    {"name": "Breakfast"},
    {"name": "Lunch"},
    {"name": "Dinner"},
    {"name": "Dessert"},
    {"name": "Snack"},
    {"name": "Appetizer"},
    {"name": "Main Course"},
    {"name": "Side Dish"},
    {"name": "Salad"},
    {"name": "Soup"},
    {"name": "Beverage"},
    {"name": "Vegetarian"},
    {"name": "Vegan"},
    {"name": "Gluten-Free"},
    {"name": "Seafood"},
]

RECIPE_DATA = [
    {
        "name": "Classic Pancakes",
        "picture": "recipe_pics/pancakes.jpg",
        "description": "Fluffy homemade pancakes perfect for a weekend breakfast.",
        "method": "Mix dry ingredients, add milk and eggs, whisk until smooth. Cook on a greased pan until golden brown on both sides.",
        "categories": ["Breakfast", "Dessert"],
    },
    {
        "name": "Grilled Chicken Salad",
        "picture": "recipe_pics/grilled_chicken_salad.jpg",
        "description": "Healthy grilled chicken served over fresh greens and vegetables.",
        "method": "Season and grill chicken. Slice and place over mixed greens, tomatoes, and onions. Drizzle with olive oil dressing.",
        "categories": ["Lunch", "Dinner", "Salad", "Healthy"],
    },
    {
        "name": "Spaghetti Bolognese",
        "picture": "recipe_pics/spaghetti_bolognese.jpg",
        "description": "Rich and hearty Italian pasta dish with meat sauce.",
        "method": "Cook ground beef with onions and garlic. Add tomato sauce and simmer. Serve over cooked spaghetti.",
        "categories": ["Dinner", "Main Course"],
    },
    {
        "name": "Vegetable Stir Fry",
        "picture": "recipe_pics/vegetable_stirfry.jpg",
        "description": "Quick and colorful vegetable stir fry packed with flavor.",
        "method": "Heat oil in a wok, add chopped vegetables, stir fry on high heat. Add soy sauce and cook until tender-crisp.",
        "categories": ["Dinner", "Vegetarian", "Vegan"],
    },
    {
        "name": "Chocolate Chip Cookies",
        "picture": "recipe_pics/cookies.jpg",
        "description": "Soft and chewy chocolate chip cookies.",
        "method": "Cream butter and sugar, add eggs and flour, fold in chocolate chips. Bake at 180°C for 10-12 minutes.",
        "categories": ["Dessert", "Snack"],
    },
]

RECIPE_INGREDIENT_DATA = [
    {"recipe": "Classic Pancakes", "ingredient": "Flour", "quantity": "2", "unit": "cups"},
    {"recipe": "Classic Pancakes", "ingredient": "Milk", "quantity": "1.5", "unit": "cups"},
    {"recipe": "Classic Pancakes", "ingredient": "Eggs", "quantity": "2", "unit": "pcs"},
    {"recipe": "Classic Pancakes", "ingredient": "Sugar", "quantity": "2", "unit": "tbsp"},
    {"recipe": "Classic Pancakes", "ingredient": "Butter", "quantity": "2", "unit": "tbsp"},

    {"recipe": "Grilled Chicken Salad", "ingredient": "Chicken Breast", "quantity": "1", "unit": "pcs"},
    {"recipe": "Grilled Chicken Salad", "ingredient": "Tomato", "quantity": "2", "unit": "pcs"},
    {"recipe": "Grilled Chicken Salad", "ingredient": "Onion", "quantity": "0.5", "unit": "pcs"},
    {"recipe": "Grilled Chicken Salad", "ingredient": "Olive Oil", "quantity": "2", "unit": "tbsp"},
    {"recipe": "Grilled Chicken Salad", "ingredient": "Salt", "quantity": "1", "unit": "tsp"},

    {"recipe": "Spaghetti Bolognese", "ingredient": "Ground Beef", "quantity": "500", "unit": "g"},
    {"recipe": "Spaghetti Bolognese", "ingredient": "Tomato", "quantity": "3", "unit": "pcs"},
    {"recipe": "Spaghetti Bolognese", "ingredient": "Onion", "quantity": "1", "unit": "pcs"},
    {"recipe": "Spaghetti Bolognese", "ingredient": "Garlic", "quantity": "2", "unit": "cloves"},
    {"recipe": "Spaghetti Bolognese", "ingredient": "Oregano", "quantity": "1", "unit": "tsp"},

    {"recipe": "Vegetable Stir Fry", "ingredient": "Onion", "quantity": "1", "unit": "pcs"},
    {"recipe": "Vegetable Stir Fry", "ingredient": "Garlic", "quantity": "2", "unit": "cloves"},
    {"recipe": "Vegetable Stir Fry", "ingredient": "Olive Oil", "quantity": "1", "unit": "tbsp"},
    {"recipe": "Vegetable Stir Fry", "ingredient": "Salt", "quantity": "0.5", "unit": "tsp"},
    {"recipe": "Vegetable Stir Fry", "ingredient": "Black Pepper", "quantity": "0.5", "unit": "tsp"},

    {"recipe": "Chocolate Chip Cookies", "ingredient": "Flour", "quantity": "2.5", "unit": "cups"},
    {"recipe": "Chocolate Chip Cookies", "ingredient": "Sugar", "quantity": "1", "unit": "cup"},
    {"recipe": "Chocolate Chip Cookies", "ingredient": "Butter", "quantity": "1", "unit": "cup"},
    {"recipe": "Chocolate Chip Cookies", "ingredient": "Eggs", "quantity": "2", "unit": "pcs"},
    {"recipe": "Chocolate Chip Cookies", "ingredient": "Milk", "quantity": "2", "unit": "tbsp"},
]

REVIEW_DATA = [
    {
        "rating": 5,
        "description": "Absolutely delicious! The pancakes were fluffy and easy to make.",
        "user": "jdoe",
        "recipe": "Classic Pancakes",
    },
    {
        "rating": 4,
        "description": "Great flavor, but I added a bit more sugar to suit my taste.",
        "user": "emilyd",
        "recipe": "Classic Pancakes",
    },
    {
        "rating": 5,
        "description": "Healthy and filling. Perfect lunch option!",
        "user": "jsmith",
        "recipe": "Grilled Chicken Salad",
    },
    {
        "rating": 3,
        "description": "Good, but I think it needed more seasoning.",
        "user": "mbrown",
        "recipe": "Grilled Chicken Salad",
    },
    {
        "rating": 5,
        "description": "Rich and hearty. Tasted just like authentic Italian pasta.",
        "user": "superadmin",
        "recipe": "Spaghetti Bolognese",
    },
    {
        "rating": 4,
        "description": "Very tasty and easy to prepare. Will make again.",
        "user": "jdoe",
        "recipe": "Spaghetti Bolognese",
    },
    {
        "rating": 4,
        "description": "Quick and healthy dinner. Loved the freshness.",
        "user": "emilyd",
        "recipe": "Vegetable Stir Fry",
    },
    {
        "rating": 2,
        "description": "It was okay, but a bit bland for my liking.",
        "user": "mbrown",
        "recipe": "Vegetable Stir Fry",
    },
    {
        "rating": 5,
        "description": "These cookies were amazing! Soft and chewy.",
        "user": "jsmith",
        "recipe": "Chocolate Chip Cookies",
    },
    {
        "rating": 4,
        "description": "Very good recipe, turned out perfectly.",
        "user": "jdoe",
        "recipe": "Chocolate Chip Cookies",
    },
]


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




