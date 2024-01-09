from django.urls import path, re_path
from . import views
from .views import *

urlpatterns = [
    path('', index, name='home'),                                           # главная страница
    path('about/', about, name='about'),                                    # страница о нас
    path('add_recipe/', add_recipe, name='add_recipe'),                     # страница добавить рецепт
    path('contact/', ContactFormView.as_view(), name='contact'),                              # страница обратной связи пользователя
    path('login/', LoginUser.as_view(), name='login'),                      # страница авторизация
    path('logout/', logout_user, name='logout'),                            # страница выход из логина
    path('recipe/<int:recipe_id>/', show_recipe, name='recipe'),            # страница для открытия полной инфо о рецепте
    path('category/<int:category_id>/', show_category, name='category'),    # страница отображает категории по id
    path('register/', RegisterUser.as_view(), name='register'),             # страница для регистрации пользователя
    path('change_recipe/<int:recipe_id>/', change_recipe, name='change_recipe'), # страница добавить рецепт только для зарегестрированных пользователей
    path('add_comment/<int:recipe_id>/', add_comment, name='add_comment'),  # добавить комментарий
    path('show_comments_recipe/<int:recipe_id>/', show_comments_recipe, name='show_comments_recipe'), # страница для открытия комментариев к рецепту
    path('delete_recipe/<int:recipe_id>/', delete_recipe, name='delete_recipe'),  # страница для удаления рецепта его автором
    path('user_recipes/', show_user_recipes, name='user_recipes'),          # страница для отображения всех  рецептов авторизоыванного пользователя
    path('recipe_publication/<int:recipe_id>, <int:published>/', recipe_publication, name='recipe_publication'),   # возможность  рецепт опубликовать и снять с публикации


]
