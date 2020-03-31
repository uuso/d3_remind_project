from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Book

# Create your views here.

def books_list(request):
    books = Book.objects.all()
    return HttpResponse(books)

def index(request):
    template = loader.get_template('index.html')
    books_count = Book.objects.count()
    bib_data = {'title': 'мою библиотэку', 'count': books_count, }
    return HttpResponse(template.render(bib_data))