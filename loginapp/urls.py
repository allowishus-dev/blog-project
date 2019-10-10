from django.urls import path
from . import views

app_name = 'loginapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('activate', views.activate, name='activate'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset', views.password_reset, name='password_reset'),
]