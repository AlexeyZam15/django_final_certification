from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Recipe, Category, RecipeCategory
from . import forms

"""
Шаблоны
Подготовьте базовый шаблон проекта и нижеперечисленные дочерние шаблоны:
● Главная с 5 случайными рецептами кратко
● Страница с одним подробным рецептом
● Страницы регистрации, авторизации и выхода пользователя
● Страница добавления/редактирования рецепта
● *другие шаблоны на ваш выбор
"""


def get_categories_sidemenu():
    categories = Category.objects.all()
    sidemenu = {'title': 'Категории',
                'menu': [{'title': category.title, 'url': reverse('category_recipes', args=[category.id])} for category
                         in categories]}
    return sidemenu


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
    sidemenu = get_categories_sidemenu()
    context = {'recipes': recipes,
               'title': 'Главная',
               'heading': '5 случайных рецептов',
               'url': 'index',
               'sidemenu': sidemenu,
               }
    return render(request, 'recipes/recipes.html', context)


def all_recipes(request):
    """
    ● Страница со всеми рецептами
    """
    recipes = Recipe.objects.all()
    paginator = get_paginator_dict(request, recipes)
    sidemenu = get_categories_sidemenu()
    context = {'recipes': paginator['page_obj'],
               'title': 'Рецепты',
               'heading': 'Все рецепты',
               'page': paginator['page'],
               'url': 'recipes',
               'sidemenu': sidemenu,
               }
    return render(request, 'recipes/recipes.html', context)


def recipe_detail(request, recipe_id):
    """
    ● Страница с одним подробным рецептом
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {'recipe': recipe,
               'title': recipe.title,
               'heading': recipe.title,
               }
    return render(request, 'recipes/recipe-detail.html', context)


def recipe_add(request):
    """
    ● Страница добавления рецепта
    """
    form = forms.RecipeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe', recipe_id=recipe.id)
    context = {'form': form,
               'title': 'Добавление рецепта',
               'heading': 'Добавление рецепта',
               }
    return render(request, 'recipes/recipe-form.html', context)


def recipe_edit(request, recipe_id):
    """
    ● Страница редактирования рецепта
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = forms.RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('recipe', recipe_id=recipe.id)
    context = {'form': form,
               'title': 'Редактирование рецепта',
               'heading': 'Редактирование рецепта',
               }
    return render(request, 'recipes/recipe-form.html', context)


def category_recipes(request, category_id):
    """
    ● Страница со всеми рецептами по выбранной категории
    """
    category = get_object_or_404(Category, id=category_id)
    category_recipes = RecipeCategory.objects.filter(category=category)
    recipes = [recipe.recipe for recipe in category_recipes]
    paginator = get_paginator_dict(request, recipes)
    sidemenu = get_categories_sidemenu()
    context = {'recipes': paginator['page_obj'],
               'title': f'Рецепты категории: {category.title}',
               'heading': f'Рецепты категории: {category.title}',
               'page': paginator['page'],
               'url': 'categories',
               'sidemenu': sidemenu,
               }
    return render(request, 'recipes/recipes.html', context)
