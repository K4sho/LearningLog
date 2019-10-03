"""Определяет схемы url для пользователей"""

from django.conf.urls import url
from django.contrib.auth import login, views as auth_views


from . import views

urlpatterns = [
    #  Страница входа
    url(r'^login/$', login, auth_views.LoginView.as_view(template_name='users/login.html'),
        name='login'),
]
