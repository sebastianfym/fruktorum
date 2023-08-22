import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from bookmark.models import Bookmark, Collection
from user.models import User


class BookmarkCollectionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_bookmark(self):
        url = "http://localhost:8000"
        response = self.client.post(reverse('bookmark-list'), {'url': url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_bookmark_to_collection(self):
        collection = Collection.objects.create(name='Test Collection', user=self.user)
        bookmark = Bookmark.objects.create(title='Test Bookmark', url='http://localhost:8000', user=self.user)
        collection.bookmarks.add(bookmark)
        response = self.client.post(reverse('collection-bookmarks', args=[collection.id, bookmark.id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(bookmark, collection.bookmarks.all())

    def test_remove_bookmark_from_collection(self):
        collection = Collection.objects.create(name='Test Collection', user=self.user)
        bookmark = Bookmark.objects.create(title='Test Bookmark', url='http://localhost:8000', user=self.user)
        collection.bookmarks.add(bookmark)
        response = self.client.delete(reverse('collection-bookmarks', args=[collection.id, bookmark.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(bookmark, collection.bookmarks.all())
