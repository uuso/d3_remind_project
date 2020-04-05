from json import loads
from django.utils import timezone
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import formset_factory
from .models import Author, Book, Publisher, Buddy
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


class AuthorList(ListView):
    model = Author
    # we can get access to Author.objects.all() in the template
    # using {{ object_list }} construction
    template_name = 'author_list.html'


class AuthorEdit(CreateView):
    """CBV-Form на основе модели.

    Способ 1. Class-based view на основе ModelForm
        а. Модель Author, форма AuthorForm(forms.ModelForm) на базе модели Author
        б. Обработчик AuthorEdit(CreateView) с указанием модели, формы, шаблона
        и success_url
    """
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('jlib:author_list')
    template_name = 'author_edit.html'

    def form_valid(self, form):
        """В случае валидности формы выполнятся эти действия:"""
        form.put_some_action()
        return super().form_valid(form)


class BuddyListView(ListView):
    model = Buddy


class BuddyUpdateView(UpdateView):
    model = Buddy  # можно раскомментировать и убрать get_object()
    # def get_object(self, queryset=None):
    #     # get_object_or_404  принимает аргументом Model, Manager, or QuerySet !!!
    #     return get_object_or_404(Buddy.objects.filter(pk=self.kwargs["pk"]))
    fields = ['full_name']
    template_name = "jlibrary/buddy_form_edit.html"

    def get_context_data(self, **kwargs):
        """Добавлено исключительно для того, чтобы из шаблона вызвать delete по pk."""
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs["pk"]
        return context


class BuddyDeleteView(DeleteView):
    model = Buddy

    def get(self, *args, **kwargs):
        """Позволяет обойти отображение шаблона для подтверждения удаления."""
        return self.post(*args, **kwargs)

    success_url = reverse_lazy("jlibrary:buddy-list")


class BuddyCreateView(CreateView):
    """CBV-Form на основе модели.

    Способ 2 (для CreateView, UpdateView, DeleteView). Class-based view без ModelForm
        а. Для работы CreateView и UpdateView - внутри модели требуется указать метод
            get_absolute_url(self), который аналогичен работа поля success_url
        б. В обработчике определить model=Buddy или метод get_object(self), а также:
            для CreateView и UpdateView - определить список fields;
            для DeleteView - определить success_url = reverse_lazy('<app_name:>author-list') -
                это необходимо, он не смотрит на метод get_absolute_url из описания модели.
        в. Описать шаблоны:
            для CreateView и UpdateView - <app_name>/templates/<app_name>/<model_name>_form.html
                Их можно разделить, если указать template_name или template_name_suffix.
            для DeleteView - <app_name>/templates/<app_name>/<model_name>_confirm_delete.html
                Можно обойти шаблон подтверждения переопределив метод get внутри DeleteView: 
                    def get(self, *args, **kwargs): 
                        return self.post(*args, **kwargs)
        г. В urls.py указать пути, причём у UpdateView, DeleteView с аргументом <pk>
    """
    model = Buddy
    # поле несовместимо с Meta внутри ModelForm, означают одно и то же
    fields = ['full_name']


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

    slug_url_kwarg = "title"
    slug_field = "title"
    # queryset = Publisher.objects.all()

    model = Publisher

    # def get_object(self, queryset=None): return get_object_or_404(Publisher, title=self.kwargs['title'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
