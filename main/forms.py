from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile, Recipe, RecipeIngredients


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('about', 'profile_picture')

class RecipeIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ('ingredient', )

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'picture', 'description', 'method')
