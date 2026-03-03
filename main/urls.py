from django.urls import path
from main import views

app_name = 'GUR'

urlpatterns = [
    path('', views.home, name='home'),
]
