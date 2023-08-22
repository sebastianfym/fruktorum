from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_authorization_user(self):
        url = reverse("authentication-authorization-user")
        response = self.client.post(url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)

    def test_authorization_user_invalid_credentials(self):
        invalid_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        url = reverse("authentication-authorization-user")
        response = self.client.post(url, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registration(self):
        new_user_data = {
            "email": "newuser@example.com",
            "password": "newpassword"
        }
        url = reverse("authentication-registration")
        response = self.client.post(url, data=new_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email=new_user_data["email"]).exists())

    def test_registration_existing_user(self):
        url = reverse("authentication-registration")
        response = self.client.post(url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_unauthorized(self):
        url = reverse("authentication-logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
