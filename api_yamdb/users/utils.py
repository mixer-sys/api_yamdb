from django.core.mail import send_mail


CHOICES = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
)


def send_mail_with_code(username, confirmation_code, email):
    send_mail(
        subject='Confirmation code is ready!',
        message=(f"Здравствуйте, {username}! "
                 f'Ваш код подтверждения: {confirmation_code}'),
        from_email='from@example.com',
        recipient_list=(email,),
        fail_silently=True,
    )
