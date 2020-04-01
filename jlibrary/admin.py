from django.contrib import admin
from .models import Book, Author, Publisher


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'author_info', 'copy_count', 'price')
    # fields = ('ISBN', 'title', 'description', 'year_release', 'author', 'copy_count', 'price')
    exclude = ('copy_count',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass
