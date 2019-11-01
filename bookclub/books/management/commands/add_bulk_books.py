import json
from getpass import getpass

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = 'Create books from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, help='Define a JSON File Path', )

    def handle(self, *args, **kwargs):
        with open(kwargs['file']) as file:
            bulk_books = json.load(file)
            for book in bulk_books:
                book_fields = book['fields']
                Book.objects.create(title=book_fields['title'], author=book_fields['author'],
                                    description=book_fields['description'],
                                    user=User.objects.get(pk=int(book_fields['user'])))
