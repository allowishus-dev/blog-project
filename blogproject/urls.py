from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from articles import views as article_views

urlpatterns = [
    path('admin/', admin.site.urls),  # raw string
    path('about/', views.about),
    # path('', views.homepage),
    path('', article_views.article_list, name="home"),
    # the one for the app
    path('accounts/', include('loginapp.urls', namespace='loginapp')),
    path('articles/', include('articles.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
