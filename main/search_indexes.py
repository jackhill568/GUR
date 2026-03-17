import datetime
from haystack import indexes
from main.models import User, Recipe, Category, Review

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    nickname = indexes.CharField(model_attr='nickname')

    def get_model(self):
        return User


