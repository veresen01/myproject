from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить рецепт", 'url_name': 'add_recipe'},
        {'title': "Ваши рецепты", 'url_name': 'user_recipes'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    # paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.annotate(Count('recipe'))

        # для исключения меню если пользователь не авторизован
        # user_menu = menu.copy()
        # if not self.request.user.is_authenticated:
        #     user_menu.pop(1)

        context['menu'] = menu

        context['categories'] = categories
        if 'category_selected' not in context:
            context['category_selected'] = 0
        return context
