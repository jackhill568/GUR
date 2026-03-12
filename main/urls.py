from django.urls import path
from main import views

app_name = 'GUR'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.add_recipe, name='upload a recipe'),
    path('register/', views.register, name='register'),
    path('recipe/search', views.register, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
