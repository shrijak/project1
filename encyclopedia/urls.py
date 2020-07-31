from django.urls import path

from . import views

app_name = "enc"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.page, name="page"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("edit/<str:name>", views.edit, name="edit")
]
