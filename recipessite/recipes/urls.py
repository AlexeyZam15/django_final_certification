from django.urls import path
from .views import index, all_recipes, recipe_detail

urlpatterns = [
    path('', index, name='index'),
    path('recipes/', all_recipes, name='recipes'),
    path('recipes/<int:recipe_id>/', recipe_detail, name='recipe'),
]
