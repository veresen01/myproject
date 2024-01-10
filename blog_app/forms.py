from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.template.context_processors import request

from .models import *


# форма добавления рецепта (связана с моделью)
class AddRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):  # заполнения пустой метки поля
        super().__init__(*args, **kwargs)
        self.fields['category_id'].empty_label = "Категория не выбрана"

    class Meta:
        model = Recipe
        exclude = ['user_login']  # исключение из формы поля пользователя
        # fields = '__all__'
        fields = ['title', 'description', 'steps_cook', 'time_cook', 'ingredients', 'image', 'is_published', 'calories',
                  'author', 'category_id', ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'steps_cook': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'ingredients': forms.Textarea(attrs={'cols': 60, 'rows': 10}),

        }

    # проверка валидации поля title в форме добавления рецепта
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Длина превышает 100 символов')
        return title


# форма для регистрации пользователя
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# форма для авторизации пользователя
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


# форма несвязанная с моделью
class ChangeRecipeForm(forms.Form):
    title = forms.CharField(required=False, max_length=200, label="Название блюда",
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    # lug = forms.SlugField(max_length=255, label="URL")
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                                  label="Описание")
    steps_cook = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                                 label="Шаги готовки")
    time_cook = forms.IntegerField(label="Готовка, мин", required=False)
    ingredients = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                                  label="Ингредиенты")
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"placeholder": "Изображение продукта"}))
    is_published = forms.BooleanField(label="Опубликовано", required=False)
    calories = forms.IntegerField(required=False, label="калории, Ккал")
    author = forms.CharField(required=False, max_length=50, label="имя автора",
                             widget=forms.TextInput(attrs={'class': 'form-input'}))
    category_id = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), label="Категории",
                                         empty_label="Категория не выбрана")


# форма добавления рецепта (связана с моделью)
class AddCommentForm(forms.Form):
    user_name = forms.CharField(required=False, max_length=200, label="имя пользователя ",
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
    # lug = forms.SlugField(max_length=255, label="URL")
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                                  label="Комментарий")
    estimation = forms.DecimalField(label="оценка (0-5)", min_value=1, max_value=5, decimal_places=1)


# форма для заполнения обратной связи
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))

