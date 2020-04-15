from django.urls import path
from .views import AuthorEdit, AuthorList, book_creators_many
from .views import PublisherLView, PublisherTView, PublisherDView
from .views import BuddyListView, BuddyCreateView, BuddyUpdateView, BuddyDeleteView
from .views import BookUpdateView

app_name = 'jlibrary'

urlpatterns = [
    path('author/', AuthorList.as_view(), name='author-list'),
    path('author/create', AuthorEdit.as_view(), name='author-create'),
    path('author/createmany', book_creators_many, name='book-creators'),
    path('buddy/', BuddyListView.as_view(), name='buddy-list'),
    path('buddy/create', BuddyCreateView.as_view(), name='buddy-create'),
    path('buddy/<int:pk>/', BuddyUpdateView.as_view(), name='buddy-edit'),
    path('buddy/<int:pk>/delete', BuddyDeleteView.as_view(), name='buddy-delete'),
    path('publishers/listview', PublisherLView.as_view()),
    path('publishers/templateview', PublisherTView.as_view()),
    path('publishers/detailview/<title>', PublisherDView.as_view()),
    path('books/<pk>/', BookUpdateView.as_view(), name='book-edit'),
]
