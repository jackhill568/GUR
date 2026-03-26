from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile, Review, Recipe, RecipeIngredients, Ingredient
from django_select2 import forms as s2forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'profile_picture')

class IngredientWidget(s2forms.ModelSelect2TagWidget):
    model = Ingredient
    search_fields = [
        'name__icontains',
    ]
    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)

        result = []
        for val in values:
            obj, _ = Ingredient.objects.get_or_create(name=val)
            result.append(obj.pk)
        return result

class RecipeForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=IngredientWidget,
        required=False                                 
    )
    class Meta:
        model = Recipe
        fields = ('name', 'picture', 'description', 'method', 'ingredients')
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'description')
        
