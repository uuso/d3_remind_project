from django.contrib import admin
from .models import Book, Author, Publisher, BookCreators


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # list_display = ('title', 'publisher', 'author_info', 'copy_count', 'price')
    list_display = ('title', 'publisher', 'authors_info', 'copy_count', 'price')
    exclude = ('copy_count',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country', 'inspired')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

@admin.register(BookCreators)
class BookCreatorsAdmin(admin.ModelAdmin):
    list_display = ("author", "book", "inspirer")