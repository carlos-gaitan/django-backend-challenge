from django.core.management.base import BaseCommand, CommandError
from books.models import Book, Author, Reviewer, Genre, Editorial, Tag
import requests
import json


def get_or_create_obj(klass, name, **kwargs):
    if not name:
        return None
    if len(klass.objects.filter(name=name)) == 0:
        kwargs['name'] = name
        obj = klass.objects.create(**kwargs)
        return obj
    return klass.objects.filter(name=name).first()


def get_tags(tags=None):
    if not tags or not isinstance(tags, list) or len(tags) == 0:
        return []
    return [get_or_create_obj(Tag, _t) for _t in tags]


class Command(BaseCommand):
    help = 'Imports the books from a dataset'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        res = requests.get('https://adminlibros.lanacion.com.ar/libros/2019/')
        if res.status_code != 200:
            raise CommandError('Cannot retrieve dataset, please try later!')
        data = res.json()
        for _item in data:
            # print(_item)
            _item.get('author')
            _author = get_or_create_obj(Author, name=_item.get('author'))
            _reviewer = get_or_create_obj(Reviewer, name=_item.get('reviewer'), link=_item.get('reviewer_link'))
            _genre = get_or_create_obj(Genre, name=_item.get('genre'))
            _editorial = get_or_create_obj(Editorial, name=_item.get('editorial'))

            book = Book.objects.create(
                title=_item.get('title'),
                text=_item.get('text'),
                slug=_item.get('slug'),
                contacted=_item.get('contacted', False),
                external_links=json.dumps(_item.get('external_links', [])),
                links=json.dumps(_item.get('links', [])),
                thumbnail=json.dumps(_item.get('thumbnail', [])),
                image=json.dumps(_item.get('image', [])),
                author=_author,
                reviewer=_reviewer,
                genre=_genre,
                editorial=_editorial,
            )
            for _t in get_tags(_item.get('tags')):
                book.tags.add(_t)
            book.save()
