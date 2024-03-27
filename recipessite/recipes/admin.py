from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Recipe, Category, RecipeCategory


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'show_image', 'time', 'category', 'created_at', 'changed_at')
    search_fields = ('title', 'author__username', 'description', 'steps')
    list_per_page = 15
    list_filter = ('author', 'time',)
    readonly_fields = ('category',)

    @admin.display(description='Изображение')
    def show_image(self, recipe: Recipe):
        if recipe.image:
            return mark_safe(f'<a href="{recipe.image.url}" ><img src="{recipe.image.url}" width="60"></a>')
        return 'отсутствует'

    @admin.display(description='Категория')
    def category(self, recipe: Recipe):
        return ', '.join([rc.category.title for rc in RecipeCategory.objects.filter(recipe=recipe)])


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'description')
    list_per_page = 15


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'category')
    search_fields = ('recipe__title', 'category__title')
    list_per_page = 15
    list_filter = ('recipe', 'category')
