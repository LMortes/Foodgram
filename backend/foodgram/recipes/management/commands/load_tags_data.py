from django.core.management import BaseCommand
from recipes.models import Tag
from csv import DictReader


class Command(BaseCommand):
    help = "Загрузка данных из tags.csv"

    def handle(self, *args, **options):
        print("Загрузка тэгов.")
        count = 0
        for row in DictReader(
            open('./data/tags.csv', encoding='utf-8')
        ):
            tag = Tag(
                name=row['name'],
                slug=row['slug'],
                color=row['color'],
            )
            tag.save()
            count += 1
        print(f'Успешно загружено {count} тэгов')
