from django.urls import path
from .views import AuthorEdit, AuthorList, book_creators_many

app_name = 'jlibrary'

urlpatterns = [
    path('author/create', AuthorEdit.as_view(), name='author_create'),
    path('author', AuthorList.as_view(), name='author_list'),
    path('author/createmany', book_creators_many, name='book_creators_many'),
]
