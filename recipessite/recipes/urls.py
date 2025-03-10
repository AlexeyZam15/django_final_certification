from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.all_recipes, name='recipes'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe'),
    path('recipes/add/', views.recipe_add, name='add_recipe'),
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit, name='edit_recipe'),
    path('recipes/<int:recipe_id>/delete/', views.recipe_delete, name='delete_recipe'),
    path('recipes/category/<int:category_id>/', views.category_recipes, name='category_recipes'),
    path('categories/', views.show_categories, name='categories'),
    path('categories/<int:category_id>/', views.category_detail, name='category'),
]
