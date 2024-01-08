from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView
from book.models import Book, Category

# Create your views here.


def home(request, category_slug=None):
    data = Book.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        data = Book.objects.filter(category=category)
    category = Category.objects.all()

    return render(request, 'home.html', {'data': data,'category':category})