from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
]

# Create your views here.