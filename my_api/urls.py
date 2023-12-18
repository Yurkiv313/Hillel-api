from django.urls import path
from .views import books, book_detail, authors, author_detail

urlpatterns = [
    path('books/', books, name='books'),
    path('books/<int:id>/', book_detail, name='book_detail'),
    path('authors/', authors, name='authors'),
    path('authors/<int:id>/', author_detail, name='author_detail'),
]