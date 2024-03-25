from django.shortcuts import render
from .models import Recipe, Category, RecipeCategory

"""
Шаблоны
Подготовьте базовый шаблон проекта и нижеперечисленные дочерние шаблоны:
● Главная с 5 случайными рецептами кратко
● Страница с одним подробным рецептом
● Страницы регистрации, авторизации и выхода пользователя
● Страница добавления/редактирования рецепта
● *другие шаблоны на ваш выбор
"""


def index(request):
    """
    ● Главная с 5 случайными рецептами кратко
    """
    recipes = Recipe.objects.order_by('?')[:5]
    context = {'recipes': recipes,
               'title': 'Главная',
               }
    return render(request, 'recipes/index.html', context)
