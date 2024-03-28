from django.urls import path
from .views import index, all_recipes

urlpatterns = [
    path('', index, name='index'),
    path('recipes/', all_recipes, name='recipes'),
]
