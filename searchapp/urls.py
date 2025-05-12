from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("result/", views.search, name="search"),
    path("ajax/search/", views.search_ajax, name="search_ajax"),
]
