from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'my_api'

urlpatterns = [
    path('books/', views.books, name='books'),
    path('books/<int:id>/', views.book_detail, name='book_detail'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:id>/', views.author_detail, name='author_detail'),
    path('docs/', TemplateView.as_view(template_name='swagger.yuml', content_type='text/yaml'), name='swagger_docs'),
]
