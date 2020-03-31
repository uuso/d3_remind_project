from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.db.models import Count
from .models import Book, Author

# Create your views here.

def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def index(request):
    template = loader.get_template('index.html')
    bib_data = {
        'title': 'мою библиотэку',
        'books': Book.objects.all()
        }
    return HttpResponse(template.render(bib_data))
