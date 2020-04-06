from django.contrib import admin
from .models import Book, Author, Publisher, BookCreator
from .models import BookLease, Buddy


admin.site.register(Publisher)
admin.site.register(Buddy)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'publisher', 'authors_info', 'copies_in_stock',
        'copies_in_lease', 'price')
    exclude = ('copy_count',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country', 'inspired')


@admin.register(BookCreator)
class BookCreatorAdmin(admin.ModelAdmin):
    list_display = ("author", "book", "inspirer")


@admin.register(BookLease)
class BookLeaseAdmin(admin.ModelAdmin):
    list_display = ("buddy", "book")
