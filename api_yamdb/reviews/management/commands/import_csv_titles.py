import os
from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Title

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the titles data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Title.objects.exists():
            print('Title data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print('Loading Title data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'titles.csv'
        )
        for row in DictReader(open(path)):
            title = Title(
                pk=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
            title.save()