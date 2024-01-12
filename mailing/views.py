from django.shortcuts import render
from django.urls import path
from . import views
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h4>hi<h4>")