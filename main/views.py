from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'main/home.html')

@login_required
def add_recipe(request):
    return HttpResponse("upload recipe")

def register(request):
    return HttpResponse("sign up")

def user_login(request):
    return HttpReponse("login")

@login_required
def user_logout(request):
    return HttpResponse("logout")


