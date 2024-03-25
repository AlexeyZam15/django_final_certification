from django.contrib import admin

from .models import Recipe, Category, RecipeCategory


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    pass
