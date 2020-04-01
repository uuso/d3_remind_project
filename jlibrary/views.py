from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.forms import formset_factory
from .models import Author, Book, Publisher
from .forms import AuthorForm, BookCreatorsForm


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
    books = Book.objects.all().select_related('publisher')
    for pub in Publisher.objects.all():
        data["publishers"].append({
            "name": str(pub),
            "books": books.filter(publisher=pub)})

    return HttpResponse(template.render(data))


def book_creators_many(request):
    BCFormset = formset_factory(BookCreatorsForm, extra=2)
    if request.method == "POST":
        bc_formset = BCFormset(
            request.POST, request.FILES, prefix="bookcreators")
        if bc_formset.is_valid():
            for form in bc_formset:
                form.save()
            return HttpResponseRedirect(reverse_lazy('jlib:author_list'))
    else:
        bc_formset = BCFormset(prefix="bookcreators")
    return render(request, template_name='book_creators_edit.html',
                  context={'bc_formset': bc_formset})


class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('jlib:author_list')
    template_name = 'author_edit.html'


class AuthorList(ListView):
    model = Author
    # we can get access to Author.objects.all() in the template
    # using {{ object_list }} construction
    template_name = 'author_list.html'


# class BookCreatorsEdit(CreateView):
#     model = BookCreators
#     form_class = BookCreatorsForm
#     success_url = reverse_lazy
