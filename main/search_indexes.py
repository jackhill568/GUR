import datetime
from haystack import indexes
from main.models import User, Recipe, Review, Category


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Category

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    nickname = indexes.CharField(model_attr='nickname')

    def get_model(self):
        return User

class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    method = indexes.CharField(model_attr='method')
    ingredients = indexes.MultiValueField()

    def get_model(self):
        return Recipe

    def prepare_ingredients(self, obj):
        return [
            ri.ingredient.name
            for ri in obj.recipeingredients_set.all()
        ]    

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ReviewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    rating = indexes.CharField(model_attr='rating')
    description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Review

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
