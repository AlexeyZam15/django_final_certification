from django.core.paginator import Paginator
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

menu = [{'title': "Главная", 'url_name': 'index'},
        {'title': "Рецепты", 'url_name': 'recipes'},
        ]


def get_paginator_dict(request, queryset):
    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj,
            'page': int(page_number)
            }


def index(request):
    """
    ● Главная с 5 случайными рецептами кратко
    """
    recipes = Recipe.objects.order_by('?')[:5]
    context = {'recipes': recipes,
               'title': 'Главная',
               'heading': '5 случайных рецептов',
               'menu': menu,
               }
    return render(request, 'recipes/recipes.html', context)


def all_recipes(request):
    """
    ● Страница со всеми рецептами
    """
    recipes = Recipe.objects.all()
    paginator = get_paginator_dict(request, recipes)
    context = {'recipes': paginator['page_obj'],
               'title': 'Рецепты',
               'heading': 'Все рецепты',
               'menu': menu,
               'page': paginator['page'],
               }
    return render(request, 'recipes/recipes.html', context)
