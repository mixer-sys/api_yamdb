import os
from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import GenreTitle

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the titles data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        if GenreTitle.objects.exists():
            print('GenreTitle data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print('Loading GenreTitle data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'genre_title.csv'
        )
        for row in DictReader(open(path)):
            genre_title = GenreTitle(
                pk=row['id'],
                genre_id=row['genre_id'],
                title_id=row['title_id'],
            )
            genre_title.save()