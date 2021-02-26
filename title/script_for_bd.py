import csv
from itertools import islice

from django.http import HttpResponse

from title.models import Category, Genre, Title


def fill_tables(request):
    # заполняем категории
    with open('data/category.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in islice(reader, 1, None):
            _, created = Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
    # заполняем жанры
    with open('data/genre.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in islice(reader, 1, None):
            _, created = Genre.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )

    with open('data/titles.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in islice(reader, 1, None):
            category = Category.objects.get(id=row[3])
            _, created = Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category,
            )
    with open('data/genre_title.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in islice(reader, 1, None):
            title_id = row[1]
            genre_id = row[2]
            genres = Genre.objects.filter(id=genre_id)
            title = Title.objects.get(id=title_id)
            title.genre.set(genres)
            title.save()

    return HttpResponse('ok')
