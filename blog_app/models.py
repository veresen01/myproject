from django.urls import reverse

from django.db import models



# модель рецепта
class Recipe(models.Model):
    user_login = models.CharField(max_length=200, default='rootRecipe')
    title = models.CharField(max_length=200, verbose_name="Заголовок*")
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание*")
    steps_cook = models.TextField(blank=True, verbose_name="Шаги")
    time_cook = models.IntegerField(verbose_name="Готовка в мин*")
    image = models.ImageField(blank=True, upload_to="images/", verbose_name='фото')
    ingredients = models.TextField(verbose_name="Ингредиенты*")
    views = models.IntegerField(default=0, verbose_name="Кол просмотров")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    change_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    calories = models.IntegerField(blank=True, verbose_name="Ккал*")
    estimation_average = models.DecimalField(default=0, max_digits=2, decimal_places=1, verbose_name="Средний бал")
    author = models.CharField(max_length=200, verbose_name="имя автора*")
    category_id = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категории*")

    def __str__(self):
        return self.title

    # формирует динамические адреса для id рецепта
    def get_absolute_url(self):
        return reverse('recipe', kwargs={'recipe_id': self.pk})

    # для admin панели
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"  # атрибут замены в admin поля Recipe
        ordering = ['-change_at', 'title']  # сортировка в admin и на сайте по полям Recipe


# модель комментария к рецепту
class Comment(models.Model):
    user_login = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    estimation = models.DecimalField(max_digits=2, decimal_places=1, )
    create_at = models.DateField(auto_now_add=True)
    change_at = models.DateField(auto_now_add=True)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'Комментарий к рецепту: {self.recipe_id}, оценка: {self.estimation}'


# модель категория
class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="категория")
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    # формирует динамические адреса для id рецепта
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'
        ordering = ['title']
