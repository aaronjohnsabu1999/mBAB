from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.search, name='search'),
    path('case/', views.caseFlip, name='caseFlip'),
    path('testChoose/<str:test>/', views.updateTestament, name='updateTestament'),
    path('bookChoose/', views.bookSelect, name='bookSelect'),
]
