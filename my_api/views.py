from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from .models import Author, Book
from .serializer.serializers import AuthorSerializer, BookSerializer


@extend_schema(request=AuthorSerializer, responses={200: AuthorSerializer(many=True)})
class AuthorViews(viewsets.ModelViewSet):
    queryset = Author.objects.all()

    @action(detail=False)
    def get_authors(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=False, methods=["post"])
    def create_authors(self, request):
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @action(detail=True)
    def author_detail_get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        return JsonResponse({"author": {"id": author.id, "name": author.name}})

    @action(detail=True, methods=["put"])
    def update_author(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        try:
            data = json.loads(request.body)
            name = data.get("name")
        except json.JSONDecodeError:
            return JsonResponse({"message": "Request body must be JSON"}, status=400)

        if not name:
            return JsonResponse(
                {"message": "Name is required. Name should not be empty"}, status=400
            )

        author.name = name
        author.save()
        return JsonResponse({"name": author.name, "id": author.id})

    @action(detail=True, methods=["delete"])
    def delete_author(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        author.delete()
        return JsonResponse({}, status=204)


@extend_schema(request=BookSerializer, responses={200: BookSerializer(many=True)})
class BooksViews(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    @action(detail=False)
    def get_books(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=False, methods=["post"])
    def create_book(self, request):
        data = json.loads(request.body)
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    # author = get_object_or_404(Author, id=author_id)
    # book = Book.objects.create(title=title, author=author)
    # return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author.name}, status=201)

    @action(detail=True)
    def book_detail_get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return JsonResponse(
            {"book": {"id": book.id, "title": book.title, "author": book.author.name}}
        )

    @action(detail=True, methods=["put"])
    def update_book(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        try:
            data = json.loads(request.body)
            title = data.get("title", book.title)
            author_id = data.get("author", book.author.id)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Request body must be JSON"}, status=400)

        if not title or not author_id:
            return JsonResponse(
                {"message": "Title and author are required"}, status=400
            )

        author = get_object_or_404(Author, id=author_id)
        book.title = title
        book.author = author
        book.save()
        return JsonResponse(
            {"id": book.id, "title": book.title, "author": book.author.name}
        )

    @action(detail=True, methods=["delete"])
    def delete_book(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return JsonResponse({}, status=204)
