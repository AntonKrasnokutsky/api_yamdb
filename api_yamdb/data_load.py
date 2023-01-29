from csv import DictReader
from django.core.management import BaseCommand, CommandError

from titles.models import Title, Category, Genre, GenreTitle


class TitleCommand(BaseCommand):

    def handle(self, *args, **options):
        file_name = 'titles.csv'

        if Title.objects.exists():
            raise CommandError('Data exists in database!')

        for row in DictReader(open(f'./static/data/{file_name}')):
            model = Title(
                id=row['id'], name=row['name'],
                year=row['year'], category=row['category']
            )
            model.save()
