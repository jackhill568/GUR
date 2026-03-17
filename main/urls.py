from django.urls import path,include
from main import views

app_name = 'GUR'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.add_recipe, name='upload a recipe'),
    path('register/', views.register, name='register'),
    path('recipe/<slug:recipe_slug>/', views.view_recipe, name='view_recipe'),
    path('user/<int:user_id>/', views.view_user, name='view_user'),
    path('search', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
