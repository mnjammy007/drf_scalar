from django.urls import path

from home.views import index, people, login

urlpatterns = [
    path("index/", index),
    path("person/", people),
    path("login/", login),
]
