from django.contrib.auth.models import User
from main.models import UserProfile, Recipe, Ingredient, Category, RecipeIngredients, Review



def add_ingredient(name: str):
    i = Ingredient.objects.get_or_create(name=name)[0]
    i.save()
    return i

def add_category(name: str):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


RECIPE_DICT = {
        "name": "NONE",
        "picture": "NONE",
        "description": "NONE",
        "method": "NONE",
        "categories": ["NONE"],
}
def add_recipe(data):
    r = Recipe.objects.get_or_create(name=data["name"])[0]
    r.picture = data["picture"]
    r.description = data["description"]
    r.method = data["method"]
    r.save()
    r.category.set(Category.objects.filter(name__in=data["categories"]))
    return r

USER_DICT = {
        "first_name": "NONE",
        "last_name": "NONE",
        "email": "NONE",
        "password": "NONE",
        "profile_picture": "NONE",
        "score": 0,
        "permission_level": 2
}
def add_user(data):
    user, created = User.objects.get_or_create(
        username=data["nickname"],
        defaults={
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
        }
    )
    if created:
        user.set_password(data.get("password") or "password123")
        user.save()

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"nickname": data["nickname"]}
    )
    profile.profile_picture = data["profile_picture"]
    profile.score = data["score"]
    profile.permission_level = data["permission_level"]
    profile.save()
    return profile

RECIPE_INGREDIENT_DICT = {
            "ingredient": "NONE",
            "recipe": "NONE",
            "quantity": "NONE",
            "unit": "NONE"
        }
def add_recipe_ingredients(data):

    ingredient = Ingredient.objects.get(name=data["ingredient"])
    recipe = Recipe.objects.get(name=data["recipe"])

    ri = RecipeIngredients.objects.get_or_create(ingredient=ingredient, recipe=recipe)[0]

    ri.quantity = data["quantity"]
    ri.unit = data["unit"]
    ri.save()
    return ri


REVIEW_DICT = {
        "user": "NONE",
        "recipe": "NONE",
        "desctiption": "NONE",
        "rating": 0
    }
def add_review(data):

    profile = UserProfile.objects.get(nickname=data["user"])
    recipe = Recipe.objects.get(name=data["recipe"])

    r = Review.objects.get_or_create(user=profile, recipe=recipe, description=data["description"], rating=data["rating"])[0]

    return r
