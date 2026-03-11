from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.db.Models import Avg


from datetime import timedelta

from django.utils import timezone

from main.models import *

def home(request):
    
    current_time = timezone.now()

    week = current_time - timedelta(days=current_time.weekday())

    month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    RecipeoftheWeek = Recipe.objects.filter(date__gte=week).annotate(avg_rating=Avg("review__rating")).order_by('-avg_rating').first()

    users_in_month = User.objects.filter(recipe__date__gte=month).distinct()
    
    CookoftheMonth = users_in_month.annotate(avg_rating=Avg("recipes__reviews__rating").order_by("-avg_rating").first()

    context_dict = {}
    context_dict["RecipeoftheWeek"] = RecipeoftheWeek
    context_dict["CookoftheMonth"] = CookoftheMonth

    response = render(request, 'main/home.html', context = context_dict)
    return response


def view_recipe(request,recipe_slug):
    context_dict = {}
    try:
        recipe = Recipe.objects.get(slug=recipe_slug)
        context_dict["recipe"] = recipe
    except Recipe.DoesNotExist:
        context_dict["recipe"] = None
    return render(request, 'main/recipe.html', context=context_dict)

def view_user(request, user_nickname):
    context_dict = {}
    try:
        user = User.objects.get(nickname=user_nickname)
        context_dict["user"] = user
    except User.DoesNotExist:
        context_dict["user"] = None
    return render(request, 'main/user.html', context=context_dict)



@login_required
def add_recipe(request):
    return HttpResponse("upload recipe")

def register(request):
    return HttpResponse("sign up")

def user_login(request):
    return HttpResponse("login")

@login_required
def user_logout(request):
    return HttpResponse("logout")


