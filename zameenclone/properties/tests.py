from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import Token

from users.models import User


class MarketplaceListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user and obtain an authentication token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

