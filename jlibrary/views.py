from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.forms import formset_factory
from .models import Author, Book, Publisher
from .forms import AuthorForm, BookCreatorForm


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
    BCFormset = formset_factory(BookCreatorForm, extra=2)
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


class PublisherLView(ListView):
    """Class-based views usage example  D6.4

    Property "template_name" provides a way to override basic path
        to template ("./templates/appname/modelname-list.html")
        with ("./templates/$template_name").

    You can access the objects by using {{ object_list }} construction
        in the template.

    """

    # template_name = "publishers_listview.html"
    model = Publisher


class PublisherTView(TemplateView):
    """Class-based views usage example  D6.4
    """

    template_name = "publishers_templateview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publishers"] = Publisher.objects.all()
        return context
