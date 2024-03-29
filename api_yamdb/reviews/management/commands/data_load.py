from csv import DictReader

from django.core.management import BaseCommand, CommandError
from django.db.models.base import ModelBase

from reviews.models import (
    Title, Category, Genre,
    GenreTitle, Comment, Review
)
from users.models import User


TABLES_DICT = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = 'Load data from csv files'

    def get_row_by_model(self, cur_model: ModelBase, row: dict):
        if isinstance(cur_model, Title):
            if 'category' in row:
                row['category'] = Category.objects.get(
                    id=int(row['category'])
                )
                return row
        elif isinstance(cur_model, Review) or isinstance(cur_model, Comment):
            if 'author' in row:
                row['author'] = User.objects.get(
                    id=int(row['author'])
                )
                return row
        return row

    def handle(self, *args, **options):
        for model, file_name in TABLES_DICT.items():
            if model.objects.exists():
                raise CommandError('Data exists in database!')
            with open(
                    f'./static/data/{file_name}',
                    encoding='utf-8'
            ) as csv_file:
                reader = DictReader(csv_file)
                data = []
                for row in reader:
                    row = self.get_row_by_model(model, row)
                    data.append(model(**row))
                model.objects.bulk_create(data)
        self.stdout.write(self.style.SUCCESS('Successfully load data'))
