from django.contrib import admin
from django.db import models
from django.forms import Textarea
from reviews.models import Comment, Review, Title, Genre, GenreTitle
from reviews.models import Category


class ViewSettings(admin.ModelAdmin):
    list_per_page = 10
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 5, 'cols': 45})},
    }


class CommentAdmin(ViewSettings):
    list_display = [field.name for field in Comment._meta.fields]
    empty_value_display = '-пусто-'


class ReviewAdmin(ViewSettings):
    list_display = [field.name for field in Review._meta.fields]
    empty_value_display = '-пусто-'


class TitleAdmin(ViewSettings):
    list_display = [field.name for field in Title._meta.fields]
    empty_value_display = '-пусто-'


class GenreAdmin(ViewSettings):
    list_display = [field.name for field in Genre._meta.fields]
    empty_value_display = '-пусто-'


class GenreTitleAdmin(ViewSettings):
    list_display = [field.name for field in GenreTitle._meta.fields]
    empty_value_display = '-пусто-'


class CategoryAdmin(ViewSettings):
    list_display = [field.name for field in Category._meta.fields]
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Category, CategoryAdmin)
