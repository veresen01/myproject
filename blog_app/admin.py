from django.contrib import admin
from .models import *


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_at', 'image', 'is_published', 'calories')
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    list_editable = ('is_published',)               # поля чтобы они были редактируемые
    list_filter = ('is_published', 'create_at')     #добавлениея в fdmin фильтра

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title',)
    search_fields = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'description', 'estimation', 'create_at', 'change_at', 'recipe_id')
    list_display_links = ('user_name',)
    search_fields = ('user_name',)




admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)

