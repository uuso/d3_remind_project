from django.urls import path
from .views import AuthorEdit, AuthorList, book_creators_many
from .views import PublisherLView, PublisherTView, PublisherDView

app_name = 'jlibrary'

urlpatterns = [
    path('author/create', AuthorEdit.as_view(), name='author_create'),
    path('author', AuthorList.as_view(), name='author_list'),
    path('author/createmany', book_creators_many, name='book_creators_many'),
    path('publishers/listview', PublisherLView.as_view()),
    path('publishers/templateview', PublisherTView.as_view()),
    path('publishers/detailview/<title>', PublisherDView.as_view()),
]
