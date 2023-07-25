from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import CHOICES


class User(AbstractUser):
    username = models.CharField(
        'Никнейм',
        max_length=25,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    date_joined = models.DateTimeField(
        'Дата регистрации',
        auto_now_add=True
    )
    role = models.PositiveSmallIntegerField(
        'Роль пользователя',
        choices=CHOICES,
        blank=True,
        null=True,
        default=3,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    is_staff = models.BooleanField(
        'Доступ',
        default=False,
        help_text='Разрешение на доступ в админ-зону.',
    )
    is_active = models.BooleanField(
        'Активен',
        default=True,
        help_text=(
            'Показатель активности аккаунта. '
            'Отсутствие "флага" означает, что аккаунт удален.'
        ),
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
