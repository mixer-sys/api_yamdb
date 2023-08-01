import os
from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import Comment

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the titles data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        if Comment.objects.exists():
            print('Comment data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print('Loading Comment data')

        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', '..',
            'static', 'data',
            'comments.csv'
        )
        for row in DictReader(open(path)):
            comment = Comment(
                pk=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            comment.save()
