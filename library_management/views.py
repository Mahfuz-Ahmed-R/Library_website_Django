from urllib import request
from django.shortcuts import redirect, render
from accounts.models import UserAccountModel
from core.models import Book, Category


def home(request, book_slug=None):
    books = Book.objects.all()
    if book_slug is not None:
        book_all = Category.objects.get(slug = book_slug)
        books = Book.objects.filter(category= book_all)
    category = Category.objects.all()
    return render(request, 'books.html', {'books': books, 'category' : category})
