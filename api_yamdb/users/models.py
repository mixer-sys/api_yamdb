from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
CHOICES = (
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Аутентифицированный пользователь'),
)


class User(AbstractUser):

    username = models.CharField(
        'Никнейм',
        max_length=25,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        'Адрес эл.почты',
        unique=True,
        max_length=254,
        blank=True
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    date_joined = models.DateTimeField(
        'Дата регистрации',
        auto_now_add=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=9,
        choices=CHOICES,
        blank=True,
        null=True,
        default='user',
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
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            ),
        )

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR
