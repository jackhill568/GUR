from django.contrib import admin
from main.models import Recipe, Category, Ingredient, RecipeIngredients, UserProfile, Review, Flag
# Register your models here.


admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredients)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Flag)
