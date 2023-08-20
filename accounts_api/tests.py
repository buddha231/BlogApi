# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User


class UserTests(APITestCase):

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/accounts/users/'
        data = {'username': 'testuser',
                'email': 'test@use.com', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().email, 'test@use.com')

    def test_create_user_without_email(self):
        pass

    def test_create_user_without_username(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/accounts/users/'
        data = {'email': 'testt@user.com', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
