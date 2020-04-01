from django.contrib import admin
from .models import Book, Author

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_info', 'copy_count', 'price')
    # fields = ('ISBN', 'title', 'description', 'year_release', 'author', 'copy_count', 'price')
    exclude = ('copy_count',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass