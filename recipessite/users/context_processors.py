from recipes.utils import get_menu


def get_recipes_context(request):
    return {'mainmenu': get_menu()}
