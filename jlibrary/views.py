from json import loads
from django.utils import timezone
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView, DetailView
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
        print(request.POST)
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
        in the template. To override construction use "context_object_name" property.

    You can change the queryset by usig "queryset" property.
        Example:
            queryset = Publisher.objects.filter(country="RU")

    Method "set_queryset(self)" can provide you a queryset filtering according
        to information from the request.
    """

    # template_name = "publishers_listview.html"
    model = Publisher

    def put(self, request):
        """HTTP method PUT receives a JSON to create new Publisher.
        *   This method doesn't work in display views.
            Use CreateView, FormView, etc instead.
        """
        data = loads(request.body)
        new_pub = self.model(**data)
        new_pub.save()


class PublisherTView(TemplateView):
    """Class-based views usage example  D6.4"""

    template_name = "publishers_templateview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["publishers"] = Publisher.objects.all()
        return context


class PublisherDView(DetailView):
    """DetailView по идее должен выдавать информацию по отдельному объекту модели.

    --- Указать объект (способ №1)
    О том, какой экземпляр будет выведен, CBV решит исходя из self.model и url доступа.
        URL должен содержать либо <pk>, либо <slug>. В первом случае поиск произведёт
        по model.pk, во втором - по model.slug.

    Переписать slug можно установив следующие свойства CBV:
        slug_url_kwarg="slug" - атрибут URL, который будет использоваться для запроса;
        slug_field="slug" - поле модели, которое будет сравниваться
            со значением slug_url_kwarg

    --- Указать объект (способ №2)
    Параметры, указанные внутри URL, передаются внутрь CBV и хранятся в self.request,
        self.args, self.kwargs. Из запроса можно вычленить параметр, например, <pub>
        из '/publishers/<slug:pub>', при помощи self.kwargs["pub"]. Это значение можно
        использовать внутри метода
            для ListView - get_queryset(self), возвращающего queryset или список
            для DetailView - get_object(self), возвращающего объект
    При использовании данного способа нет необходимости указывать model = Publisher,
        но в таком случае потребуется вручную указать шаблон.

    --- Указать объект (способ №3) - для ListView
    Указание внутри CBV свойства model = Publisher эквивалентно определению запроса
        как queryset = Publisher.objects.all(). Если указать вручную свойство queryset
        или метод get_queryset(), то нет необходимости даже привязывать CBV к модели.
        Похоже, при использовании get_queryset() появляется неоднозначность в выборе шаблона
        (требуется указать свойство template_name). Со свойством такого поведения нет.


    Метод get_context_data(self, **kwargs) позволяет наполнить контекст шаблона
        дополнительными полями. Если где-то уже делаются запросы, удобно сохранять информацию
        для передачи между методами в self, например, как в примере:
        https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-display/#dynamic-filtering

    Внутри шаблона обращение к экземпляру через {{ object }}. Это имя можно переписать
        указав свойство context_object_name="object".
    """

    # slug_url_kwarg = "title"
    # slug_field = "title"
    # queryset = Publisher.objects.all()

    model = Publisher

    def get_object(self, queryset=None):
        # return Publisher.objects.filter(
        #   title=self.kwargs["title"]).first() # выведет шаблон даже без найденного объекта

        # если не найдёт объект - ошибка 404
        return get_object_or_404(Publisher, title=self.kwargs['title'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
