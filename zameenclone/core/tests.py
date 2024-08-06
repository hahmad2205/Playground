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
        self.amenities = AmenityFactory.create_batch(3)
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(
            response.data,
            [
                {'id': 1, 'name': 'Amenity 0'},
                {'id': 2, 'name': 'Amenity 1'},
                {'id': 3, 'name': 'Amenity 2'}
            ]
        )

    def test_get_no_amenity(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_result_not_paginated(self):
        response = self.client.get(self.base_url)
        self.assertNotIn("next", response.data)
        self.assertNotIn("count", response.data)


class AmenityOptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.amenity = AmenityFactory()
        self.amenity_options = AmenityOptionFactory.create_batch(3, amenity=self.amenity, is_active=True)
        self.amenity_options.extend(AmenityOptionFactory.create_batch(3, amenity=self.amenity, is_active=False))

    def test_get_amenity_option(self):
        url = reverse("amenity_options", kwargs={"pk": self.amenity.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        print(response.data)
        self.assertEqual(
            response.data,
            [
                {'id': 1, 'amenity': {'id': 1, 'name': 'Amenity 1'}, 'option': 'Option 6'},
                {'id': 2, 'amenity': {'id': 1, 'name': 'Amenity 1'}, 'option': 'Option 7'},
                {'id': 3, 'amenity': {'id': 1, 'name': 'Amenity 1'}, 'option': 'Option 8'}
            ]

        )

    def test_get_no_amenity_option(self):
        url = reverse("amenity_options", kwargs={"pk": 5})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {'detail': ErrorDetail(string='No Amenity matches the given query.', code='not_found')}
        )

    def test_result_not_paginated(self):
        url = reverse("amenity_options", kwargs={"pk": self.amenity.pk})
        response = self.client.get(url)
        self.assertNotIn("next", response.data)
        self.assertNotIn("count", response.data)

    def test_get_active_amenity_options(self):
        url = reverse("amenity_options", kwargs={"pk": self.amenity.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(
            response.data,
            [
                {'id': 1, 'amenity': {'id': 1, 'name': 'Amenity 0'}, 'option': 'Option 0'},
                {'id': 2, 'amenity': {'id': 1, 'name': 'Amenity 0'}, 'option': 'Option 1'},
                {'id': 3, 'amenity': {'id': 1, 'name': 'Amenity 0'}, 'option': 'Option 2'}
            ]
        )
