from .models import Category

menu = [{'title': "Главная", 'url_name': 'index'},
        {'title': "Рецепты", 'url_name': 'recipes'},
        {'title': "Категории", 'url_name': 'categories'}
        ]

usermenu = menu + [
    {'title': 'Добавить рецепт', 'url_name': 'add_recipe'},
]


def get_cats_menu():
    return [{'title': category.title, 'url_name': f'recipes {category.id} '} for category in Category.objects.all()]
