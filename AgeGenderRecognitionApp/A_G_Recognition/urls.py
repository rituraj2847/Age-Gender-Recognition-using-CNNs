from django.conf.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  re_path('^$', views.home, name='home'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
