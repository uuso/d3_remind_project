from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import path, include
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
    path('accounts/', include('allauth.urls')),
    path('favicon.ico', RedirectView.as_view(url="/static_url/favicon.ico")), # можно добавить permanent=True для изменения HTTP кода
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
