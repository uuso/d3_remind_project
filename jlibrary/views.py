from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
# from django.db.models import Count
from .models import Book, Publisher

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
    # добавлять request в рендеринг необходимо для вставки SCRF токена в страницу
    return HttpResponse(template.render(bib_data, request))


def book_inc(request):
    if request.method == "POST":
        book_id = request.POST['id']
        if book_id:
            book = Book.objects.get(id=book_id)
            if book:
                book.copy_count += 1
                book.save()
    return redirect('/index/')


def book_dec(request):
    if request.method == "POST":
        book_id = request.POST['id']
        if book_id:
            book = Book.objects.get(id=book_id)
            if book and book.copy_count > 0:
                book.copy_count -= 1
                book.save()
    return redirect('/index/')


def show_pubs(request):
    template = loader.get_template('show_publishers.html')

    data = {"publishers": []}
    for pub in Publisher.objects.all():
        data["publishers"].append({
            "name": str(pub),
            "books": Book.objects.filter(publisher=pub)})

    return HttpResponse(template.render(data))
