from recipes.utils import menu, usermenu


def get_recipes_context(request):
    return {'mainmenu': menu, 'usermenu': usermenu}
