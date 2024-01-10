from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
import logging
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy

from blog_app.models import Category, Recipe, Comment
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect

from .utils import DataMixin

logger = logging.getLogger(__name__)  # переменная для логирования

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить рецепт", 'url_name': 'add_recipe'},
        {'title': "Ваши рецепты", 'url_name': 'user_recipes'},
        {'title': "Обратная связь", 'url_name': 'contact'},

        ]


# вывод всех опубликованных  рецептов
def index(request):
    recipes = Recipe.objects.filter(is_published=True)  # вывод только опубликованных рецептов
    categories = Category.objects.all()

    # пагинация по 3 рецепта на 1 страницу
    paginator = Paginator(recipes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # список рецептов на текущей страницу

    context = {
        'recipes': recipes,
        'categories': categories,
        'menu': menu,
        'title': 'Главная страница',
        'category_selected': 0,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'blog_app/index.html', context=context)


# страница о сайте
def about(request):
    categories = Category.objects.all()
    context = {
        'menu': menu,
        'title': 'о сайте',
        'categories': categories,

    }

    return render(request, 'blog_app/about.html', context=context)


# добавление рецепта авторизованным пользователем-автором
def add_recipe(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            try:
                # Recipe.objects.create(**form.cleaned_data)      #запись значений из формы в БД в случае когда форма не связана с моделью

                recipe = form.save()  # запись значений из формы в БД в случае когда форма  связана с моделью через class Metta
                recipe.user_login = request.user.username
                recipe.save()
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления рецепта')
    else:
        form = AddRecipeForm()

    context = {
        'menu': menu,
        'title': 'Добавить рецепт',
        'categories': categories,
        'form': form,

    }

    return render(request, 'blog_app/add_recipe.html', context=context)


# организация обратной связи с пользователем
# def contact(request):
#     return HttpResponse("Обратная связь")


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'blog_app/contact.html'
    success_url = reverse_lazy('home')  # при успешной заполнении фомы перенаправление на домашнюю страницу

    # формирование контекста для шаблонв
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['menu'] = menu
        print(context)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    # вызов метоа приуспешной заполнении формы обратной связи
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# вывод рецeпта по id
def show_recipe(request, recipe_id):
    comments = Comment.objects.filter(recipe_id=recipe_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    categories = Category.objects.all()
    recipe.views += 1
    sum = 0
    count = 0
    if (comments):
        for comment in comments:
            sum += comment.estimation
            count += 1
        recipe.estimation_average = round(sum / count, 1)
    else:
        recipe.estimation_average = 0
    recipe.save()

    context = {
        'recipe': recipe,
        'categories': categories,
        'menu': menu,
        'title': recipe.title,
        'category_selected': recipe.category_id.id,
    }
    return render(request, 'blog_app/recipe.html', context=context)


# вывод всех опубликованных категорий и рецептов
def show_category(request, category_id):
    recipes = Recipe.objects.filter(category_id_id=category_id, is_published=True)
    categories = Category.objects.all()

    # пагинация по 3 рецепта на 1 страницу
    paginator = Paginator(recipes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # список рецептов на текущей страницу

    # если нет постов, то выдает исключение, прписанное ранее
    # if len(recipes) == 0:
    #     #raise Http404()

    context = {
        'recipes': recipes,
        'categories': categories,
        'menu': menu,
        'title': 'Все опубликованные рецепты по категориям',
        'category_selected': category_id,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'blog_app/index.html', context=context)


# регистрация пользователя
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'blog_app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    # автоматическая авторизация при успешной регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # авторризация пользователя
        return redirect('home')


# авторизация пользователдя
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'blog_app/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    # при завершении регистрации переходит на главную страницу
    def get_success_url(self):
        return reverse_lazy('home')


# выход из авторизации
def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# редактирование рецепта авторизованным пользователем
def change_recipe(request, recipe_id: int):
    categories = Category.objects.all()
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.user_login == request.user.username:
        if request.method == "POST":
            form = ChangeRecipeForm(request.POST, request.FILES)
            if form.is_valid():
                if request.POST["title"]:
                    recipe.title = request.POST["title"]
                if request.POST["description"]:
                    recipe.description = request.POST["description"]
                if request.POST["steps_cook"]:
                    recipe.steps_cook = request.POST["steps_cook"]
                if request.POST["time_cook"]:
                    recipe.time_cook = request.POST["time_cook"]
                if request.POST["author"]:
                    recipe.author = request.POST['author']
                if request.POST["ingredients"]:
                    recipe.ingredients = request.POST['ingredients']
                if request.POST["calories"]:
                    recipe.calories = request.POST['calories']
                if "image" in request.FILES:
                    recipe.image = request.FILES["image"]  # запись Image в переменную БД
                if request.POST["category_id"]:
                    recipe.category_id = form.cleaned_data['category_id']
                recipe.is_published = form.cleaned_data['is_published']

                recipe.save()
                # logger.info(f"Recipe {recipe.title} is changed successfully")
                return redirect("recipe", recipe_id=recipe.id)
        else:
            form = ChangeRecipeForm()

        context = {
            "form": form,
            "recipe": recipe,
            "menu": menu,
            'categories': categories,
            'title': 'Редактировать рецепт',
        }
    else:
        content = 'Изменить рецепт может только автор. '
        context = {
            "content": content,
            "recipe": recipe,
            "menu": menu,
            'categories': categories,
            'title': 'Редактировать рецепт',
        }

    return render(request, "blog_app/change_recipe.html", context=context)


# создание комментария к рецепту
def add_comment(request, recipe_id: int):
    categories = Category.objects.all()
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':

        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            if request.user.is_authenticated:
                comment.user_login = request.user
            else:
                comment.user_login = 'незарегистрированный пользователь'
            comment.user_name = request.POST["user_name"]
            comment.description = request.POST["description"]
            comment.estimation = request.POST["estimation"]
            comment.recipe_id = recipe
            comment.save()
            print(comment)
            # logger.info(f"Recipe {recipe.title} is changed successfully")
            return redirect("recipe", recipe_id=recipe.id)
    else:
        form = AddCommentForm()

    context = {
        "form": form,
        "recipe": recipe,
        "menu": menu,
        'categories': categories,
        'title': 'Добавить комментарий',
    }
    return render(request, "blog_app/add_comment.html", context=context)


# вывод комментариев для данного рецепта по
def show_comments_recipe(request, recipe_id):
    categories = Category.objects.all()
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = Comment.objects.filter(recipe_id=recipe)
    context = {
        'recipe': recipe,
        'menu': menu,
        'comments': comments,
        'categories': categories,
        'title': 'Kомментарии',
    }
    return render(request, 'blog_app/show_comments_recipe.html', context=context)


# удаление рецепта его автором
def delete_recipe(request, recipe_id):
    categories = Category.objects.all()
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipes = Recipe.objects.filter(user_login=request.user.username)

    if recipe.user_login == request.user.username:

        recipe.delete()
        context = {
            'recipe': recipe,
            'menu': menu,
            'categories': categories,
            'massage': 'успешно удален',
            'recipes': recipes,
            'title': 'Удаление рецепта'

        }
    else:
        context = {
            'recipe': recipe,
            'menu': menu,
            'categories': categories,
            'massage': 'удалить невозможно, так как вы не являетесь его автором.',
            'recipes': recipes,
            'title': 'Удаление рецепта'
        }
    return render(request, 'blog_app/delete_recipe.html', context=context)


# вывод всех рецептов (опубликованных и неопубликованных) конкретного автора
def show_user_recipes(request):
    recipes = Recipe.objects.filter(user_login=request.user.username)  # рецепты авторизованного пользователя
    categories = Category.objects.all()

    # пагинация по 3 рецепта на 1 страницу
    paginator = Paginator(recipes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # список рецептов на текущей страницу

    context = {
        'recipes': recipes,
        'categories': categories,
        'menu': menu,
        'title': 'Ваши рецепты',
        'category_selected': 0,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'blog_app/user_recipes.html', context=context)


def recipe_publication(request, recipe_id, published):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if published == 1:
        recipe.is_published = 'False'
    else:
        recipe.is_published = 'True'
    recipe.save()
    return redirect("recipe", recipe_id=recipe.id)
