from rest_framework import status
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase, APIClient

from users.factory import UserFactory
from core.factory import AmenityFactory, AmenityOptionFactory


class AmenityTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.base_url = reverse("amenities")

    def test_get_amenity(self):
        self.amenity = AmenityFactory()
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data[0])
        self.assertEqual("Amenity", response.data[0]["name"].split(" ")[0])


    def test_get_no_amenity(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class AmenityOptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.amenity = AmenityFactory()
        amenity_option = AmenityOptionFactory(amenity=self.amenity)

    def test_get_amenity_option(self):
        url = reverse("amenity_options", kwargs={"pk": self.amenity.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("option", response.data[0])
        self.assertEqual("Option", response.data[0]["option"].split(" ")[0])

    def test_get_no_amenity_option(self):
        url = reverse("amenity_options", kwargs={"pk": 5})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        expected_error = {'detail': ErrorDetail(string='No Amenity matches the given query.', code='not_found')}
        self.assertEqual(response.data, expected_error)

