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
    title = models.CharField(max_length=100, unique=True, verbose_name='Название', default='Название')
    description = models.TextField(max_length=1000, verbose_name='Описание', default='Описание')
    steps = models.TextField(max_length=1000, verbose_name='Шаги приготовления', default='Шаги приготовления')
    time = models.DurationField(verbose_name='Время приготовления', default="00:05:00")
    image = models.ImageField(upload_to='photos', blank=True, null=True, verbose_name='Изображение')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    changed_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    categories = models.ManyToManyField('Category', verbose_name='Категории', through='RecipeCategory')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def short(self):
        # Краткое описание
        # Возвращает первые 10 слов из описания
        return ' '.join(self.description.split()[:15]) + '...' if len(
            self.description.split()) > 15 else self.description

    def is_changed(self):
        # Проверяет, изменился ли рецепт
        # Возвращает True, если рецепт изменился, иначе False
        return self.changed_at != self.created_at

    @property
    def get_categories(self):
        # Возвращает список категорий рецепта
        return [category for category in self.categories.all()]

    @staticmethod
    def get_fields():
        return ['title', 'description', 'steps', 'image', 'time', 'categories']


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

    def short(self):
        # Краткое описание
        # Возвращает первые 10 слов из описания
        return ' '.join(self.description.split()[:30]) + '...' if len(
            self.description.split()) > 30 else self.description

    def recipes(self):
        # Возвращает рецепты категории
        # Возвращает множество рецептов
        return RecipeCategory.objects.filter(category=self).values_list('recipe', flat=True)

    def last_created_recept_date(self):
        # Возвращает дату последнего рецепта категории
        # Возвращает дату или None, если рецептов нет
        recipes = RecipeCategory.objects.filter(category=self).values_list('recipe', flat=True)
        if recipes:
            return Recipe.objects.filter(id__in=recipes).order_by('-created_at').first().created_at
        return None


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
