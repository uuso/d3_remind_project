from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import path, include, reverse_lazy

from jlibrary import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.to_index),
    path('', include('jlibrary.urls', namespace='jlib')),
    path('common/', include('common.urls', namespace='common')),
    path('index/', views.index, name="index"),
    path('index/book_increment/', views.book_inc),
    path('index/book_decrement/', views.book_dec),
    path('index/publishers/', views.show_pubs),
    path('favicon.ico', RedirectView.as_view(url="/static_url/favicon.ico")),
    path('accounts/signup/', RedirectView.as_view(url=reverse_lazy("common:user-register"),
        permanent=True)),
    path('accounts/', include('allauth.urls')),
    # по-умолчанию на пути accounts/signup/ висит встроенный в allauth
    # вью регистрации, надо перенаправить на наш:
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
