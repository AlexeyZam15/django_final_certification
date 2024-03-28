from recipes.utils import menu


def get_recipes_context(request):
    return {'mainmenu': menu}
