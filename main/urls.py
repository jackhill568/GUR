from django.urls import path, include
from main import views

app_name = 'GUR'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.add_recipe, name='upload'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('recipe/<slug:recipe_slug>/', views.view_recipe, name='view_recipe'),
    path('user/<int:user_id>/', views.view_user, name='view_user'),
    path('search', views.search, name='search'),
    path('recipe/<slug:recipe_slug>/add_review/', views.add_review, name='add_review'),
    # Moderation
    path('moderation/', views.admin_dashboard, name='admin_dashboard'),
    path('moderation/recipe/<slug:recipe_slug>/delete/', views.admin_delete_recipe, name='admin_delete_recipe'),
    path('moderation/recipe/<slug:recipe_slug>/resolve/', views.admin_resolve_recipe_flags, name='admin_resolve_recipe_flags'),
    path('moderation/recipe/<slug:recipe_slug>/resolve2/', views.admin_resolve_recipe, name='admin_resolve_recipe'),
    path('moderation/review/<int:review_id>/delete/', views.admin_delete_review, name='admin_delete_review'),
    path('moderation/review/<int:review_id>/resolve/', views.admin_resolve_review_flags, name='admin_resolve_review_flags'),
    path('moderation/review/<int:review_id>/resolve2/', views.admin_resolve_review, name='admin_resolve_review'),
    path('moderation/user/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('moderation/user/<int:user_id>/resolve/', views.admin_resolve_user_flags, name='admin_resolve_user_flags'),
    path('moderation/user/<int:user_id>/resolve2/', views.admin_resolve_user, name='admin_resolve_user'),
    # Flags
    path('recipe/<slug:recipe_slug>/flag/', views.flag_recipe, name='flag_recipe'),
    path('review/<int:review_id>/flag/', views.flag_review, name='flag_review'),
    path('user/<int:user_id>/flag/', views.flag_user, name='flag_user'),
]
