import os
from csv import DictReader

from django.core.management import BaseCommand

from users.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the titles data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.exists():
            print('User data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print('Loading User data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'users.csv'
        )
        for row in DictReader(open(path)):
            user = User(
                pk=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            user.save()