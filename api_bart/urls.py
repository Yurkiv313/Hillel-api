"""
URL configuration for api_bart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from my_api.views import AuthorViews, BooksViews

authors = AuthorViews.as_view(
    {
        "get": "get_authors",
        "post": "create_authors",
    }
)

authors_details = AuthorViews.as_view(
    {
        "get": "author_detail_get",
        "put": "update_author",
        "delete": "delete_author",
    }
)

books = BooksViews.as_view(
    {
        "get": "get_books",
        "post": "create_book",
    }
)

books_details = BooksViews.as_view(
    {
        "get": "book_detail_get",
        "put": "update_book",
        "delete": "delete_book",
    }
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/authors/", authors, name="authors"),
    path("api/authors/<int:pk>/", authors_details, name="authors_details"),
    path("api/books/", books, name="books"),
    path("api/books/<int:pk>/", books_details, name="books_details"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
