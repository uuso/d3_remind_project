from django.urls import path
from .views import AuthorEdit, AuthorList

app_name = 'jlibrary'

urlpatterns = [
    path('author/create', AuthorEdit.as_view(), name='author_create'),
    path('author', AuthorList.as_view(), name='author_list'),
]
