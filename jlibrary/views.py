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
    books_count = Book.objects.count()
    bib_data = {
        'title': 'мою библиотэку', 
        'count': books_count, 
        'answers': [q1(), q2(), q3(), q4(), q5(), q6()],        
        }
    return HttpResponse(template.render(bib_data))

def q1():    
    return { 
        'q': "Сколько стоит самая дорогая книга?",
        'a': Book.objects.order_by('price').first().price
    }

def q2():    
    return {
        'q':"Сколько в библиотеке копий самой дешёвой книги?",
        'a': Book.objects.order_by('-price').first().price
    }

def q3():    
    A2 = Author.objects.annotate(Count('book')).filter(book__count__gt = 1)
    return {
        'q': "Сколько стоят все библиотечные книги авторов, у которых больше одной книги?",
        'a': sum([b.copy_count*b.price for b in Book.objects.filter(author__in = A2)])
    }

def q4():    
    return {
        'q': "Сколько стоят все библиотечные книги иностранных писателей?",
        'a': sum([b.copy_count*b.price for b in Book.objects.exclude(author__country__exact = 'RU')])
    }

def q5():    
    return {
        'q': "Сколько стоят все экземпляры Пушкина в бибилотеке",
        'a': sum([b.price*b.copy_count for b in Book.objects.filter(author__full_name__contains = 'Пушкин')])
    }
    
def q6():
    return {
        'q': "Сколько стоят все книги, автор которых Douglas Adams? Не учитывайте стоимость копий.",
        'a': sum([b.price for b in Book.objects.filter(author__full_name__contains = 'Douglas Adams')])
    }
    
    