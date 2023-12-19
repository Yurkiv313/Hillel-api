from django.test import TestCase, Client
from django.urls import reverse
from .models import Author, Book
import json


class MyApiTests(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='Author 1')
        self.author2 = Author.objects.create(name='Author 2')
        self.book1 = Book.objects.create(title='Book 1', author=self.author1)
        self.book2 = Book.objects.create(title='Book 2', author=self.author2)

        self.client = Client()

    def test_authors_endpoint(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('authors', data)
        self.assertEqual(len(data['authors']), 2)

    def test_author_creation_endpoint(self):
        new_author_data = {'name': 'New Author'}
        response = self.client.post(reverse('authors'), json.dumps(new_author_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], new_author_data['name'])

    def test_author_detail_endpoint(self):
        response = self.client.get(reverse('author_detail', args=[self.author1.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('author', data)
        self.assertIn('id', data['author'])
        self.assertEqual(data['author']['id'], self.author1.id)
        self.assertIn('name', data['author'])
        self.assertEqual(data['author']['name'], 'Author 1')

    def test_author_update_endpoint(self):
        updated_author_data = {'name': 'Updated Author'}
        response = self.client.put(
            reverse('author_detail', args=[self.author1.id]),
            json.dumps(updated_author_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], updated_author_data['name'])
        self.assertEqual(data['id'], self.author1.id)

    def test_author_deletion_endpoint(self):
        response = self.client.delete(reverse('author_detail', args=[self.author1.id]))
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(id=self.author1.id)
