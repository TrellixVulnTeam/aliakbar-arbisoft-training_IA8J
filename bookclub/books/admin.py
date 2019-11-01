from django.contrib import admin
from books.models import Book


class CustomBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'description', 'user')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomBookAdmin, self).get_inline_instances(request, obj)


admin.site.register(Book, CustomBookAdmin)
