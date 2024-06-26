from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from users.utils import current_year


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        help_text='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        'Год произведения',
        blank=True,
        null=True,
        db_index=True,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(current_year)),
        help_text='Год произведения'
    )
    description = models.TextField(
        'Описание произведения',
        max_length=1000,
        blank=True,
    )
    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанр',
        through='GenreTitle',
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        help_text='Категория'
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        help_text='Название категории'
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=50,
        unique=True,
        help_text=('Идентификатор категории; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категориии'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres'
    )

    def __str__(self):
        return f'{self.genre}{self.title}'


class Genre(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        help_text='Название жанра'
    )
    slug = models.SlugField(
        'Идентификатор',
        max_length=50,
        unique=True,
        help_text=('Идентификатор жанра; '
                   'разрешены символы латиницы, цифры, '
                   'дефис и подчёркивание.')
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Заголовок',
        on_delete=models.CASCADE,
        help_text='Заголовок отзыва',
        related_name='reviews'
    )
    text = models.TextField(
        'Текст',
        help_text='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        help_text='Автор отзыва',
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=(
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            ),
        )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        help_text='Отзыв',
        related_name='comments'

    )
    text = models.TextField(
        'Текст',
        help_text='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        help_text='Автор комментария',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации комментария'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
