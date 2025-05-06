from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("result/", views.search, name="search"),
    path("case/", views.case_flip, name="case_flip"),
    path("testChoose/<str:test>/", views.update_testament, name="update_testament"),
    path("bookChoose/", views.book_select, name="book_select"),
]
