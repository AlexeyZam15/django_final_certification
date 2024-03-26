from datetime import datetime

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
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    steps = models.TextField(max_length=1000, verbose_name='Шаги приготовления')
    time = models.DurationField(verbose_name='Время приготовления')
    image = models.FileField(upload_to='photos', blank=True, null=True, verbose_name='Изображение')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'


class Category(models.Model):
    """
    ● *Категории рецептов
    ○ Название
    ○ *другие поля на ваш выбор
    """
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    description = models.TextField(max_length=1000, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class RecipeCategory(models.Model):
    """
    ● *Связующая таблица для связи Рецептов и Категории
    ○ *обязательные для связи поля
    ○ *другие поля на ваш выбор
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.recipe} - {self.category}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'связь рецепта и категории'
        verbose_name_plural = 'связи рецепта и категории'
