from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .models import Author, Book


def authors(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        return JsonResponse({'authors': [{'id': a.id, 'name': a.name} for a in authors]})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Request body must be JSON'}, status=400)

        if not name:
            return JsonResponse({'message': 'Name is required. Name should not be empty'}, status=400)

        author = Author.objects.create(name=name)
        return JsonResponse({'name': author.name, 'id': author.id}, status=201)


def author_detail(request, id):
    author = get_object_or_404(Author, id=id)

    if request.method == 'GET':
        return JsonResponse({'author': {'id': author.id, 'name': author.name}})

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            name = data.get('name')
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Request body must be JSON'}, status=400)

        if not name:
            return JsonResponse({'message': 'Name is required. Name should not be empty'}, status=400)

        author.name = name
        author.save()
        return JsonResponse({'name': author.name, 'id': author.id})

    elif request.method == 'DELETE':
        author.delete()
        return JsonResponse({}, status=204)


def books(request):
    if request.method == 'GET':
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        books = Book.objects.filter(title__icontains=title, author__name__icontains=author)
        return JsonResponse({'books': [{'id': b.id, 'title': b.title, 'author': b.author.name} for b in books]})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            author_id = data.get('author')
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Request body must be JSON'}, status=400)

        if not title or not author_id:
            return JsonResponse({'message': 'Title and author are required'}, status=400)

        author = get_object_or_404(Author, id=author_id)
        book = Book.objects.create(title=title, author=author)
        return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author.name}, status=201)


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == 'GET':
        return JsonResponse({'book': {'id': book.id, 'title': book.title, 'author': book.author.name}})

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            title = data.get('title', book.title)
            author_id = data.get('author', book.author.id)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Request body must be JSON'}, status=400)

        if not title or not author_id:
            return JsonResponse({'message': 'Title and author are required'}, status=400)

        author = get_object_or_404(Author, id=author_id)
        book.title = title
        book.author = author
        book.save()
        return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author.name})

    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({}, status=204)