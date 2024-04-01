from django.urls import reverse

from .models import Category


class MenuLink:
    def __init__(self, title, url, sub_menu=None):
        self.title = title
        self.url = url
        self.sub_menu = sub_menu


menu = [MenuLink('Главная', reverse('index')),
        MenuLink('Рецепты', reverse('recipes'), [MenuLink('Добавить рецепт', reverse('add_recipe')), ]),
        ]


def get_menu():
    """
    ● Меню для шапки сайта
    """
    return menu + [MenuLink('Категории', reverse('categories'),
                            [MenuLink(category.title, reverse('category', args=(category.id,))) for category in
                             Category.objects.all()])]
