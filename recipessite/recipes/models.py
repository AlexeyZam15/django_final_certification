from django.db import models

"""
Модели
Для работы с пользователями используйте встроенного в Django User`a.
Подготовьте нижеперечисленные модели:
"""


class Recipe(models.Model):
    """
    ● Рецепты:
    ○ Название
    ○ Описание
    ○ Шаги приготовления
    ○ Время приготовления
    ○ Изображение
    ○ Автор
    ○ *другие поля на ваш выбор, например ингредиенты и т.п.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    steps = models.TextField()
    time = models.IntegerField()
    image = models.ImageField(upload_to='recipes/')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    """
    ● *Категории рецептов
    ○ Название
    ○ *другие поля на ваш выбор
    """
    title = models.CharField(max_length=255)
    description = models.TextField()


class RecipeCategory(models.Model):
    """
    ● *Связующая таблица для связи Рецептов и Категории
    ○ *обязательные для связи поля
    ○ *другие поля на ваш выбор
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
