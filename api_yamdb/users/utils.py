from django.core.mail import send_mail

from api_yamdb.settings import FROM_EMAIL

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

CHOICES = (
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь'),
)


def send_mail_with_code(username, confirmation_code, email):
    send_mail(
        subject='Confirmation code is ready!',
        message=(f'Здравствуйте, {username}! '
                 f'Ваш код подтверждения: {confirmation_code}'),
        from_email=FROM_EMAIL,
        recipient_list=(email,),
        fail_silently=True,
    )
