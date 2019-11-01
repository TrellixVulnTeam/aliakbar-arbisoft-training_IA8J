from django.shortcuts import get_object_or_404, render

from books.models import Book


class UserAuthenticationMiddleware(object):
    def process_request(self, request):
        book = get_object_or_404(Book, pk=request.POST['book_id'])
        if request.user != book.user:
            error_message = 'You are not allowed to edit. Please Login with another account. '
            return render(request, 'books/edit.html', {'error_message': error_message})
