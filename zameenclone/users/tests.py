
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.factory import UserFactory


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.login_url = reverse("token_obtain_pair")

    def test_login_with_valid_credentials(self):
        data = {
            "username": self.user.username,
            "password": "defaultpassword"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_with_invalid_credentials(self):
        data = {
            "username": self.user.username,
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)


class RefreshTokenTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)

    def test_refresh_with_valid_refresh_token(self):
        data = {
            "refresh": self.refresh_token
        }
        response = self.client.post(reverse("token_refresh"), data, format='json')
        self.assertIn("access", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_with_invalid_refresh_token(self):
        data = {
            "refresh": "invalid_refresh_token"
        }
        response = self.client.post(reverse("token_refresh"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)

