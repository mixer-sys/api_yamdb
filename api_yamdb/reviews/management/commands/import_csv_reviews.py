import os
from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Review

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the titles data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Review.objects.exists():
            print('Review data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print('Loading Review data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'review.csv'
        )
        for row in DictReader(open(path)):
            review = Review(
                pk=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()