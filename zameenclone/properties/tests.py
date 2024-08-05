from django.urls import reverse
from django.core import mail

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch

from properties.enums import MobileState
from properties.models import PropertyOffers
from properties.factory import (
    PropertyImagesFactory,
    PropertyAmenityFactory,
    PropertyFactory,
    PropertyOfferFactory
)
from users.factory import UserFactory


class OfferCreateTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(self.user)
        self.image = PropertyImagesFactory()
        self.amenities = PropertyAmenityFactory()
        self.property = PropertyFactory()

    def test_create_offer(self):
        url = reverse("create_offer_generic_api")
        data = {
            "price": 500000,
            "property": self.property.id,
            "is_active": True,
            "state": "pending"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PropertyOffers.objects.count(), 1)
        offer = PropertyOffers.objects.get()
        self.assertEqual(offer.price, 500000)
        self.assertEqual(offer.offered_by, self.user)
        self.assertEqual(offer.property, self.property)
        self.assertEqual(offer.is_active, True)
        self.assertEqual(offer.state, "pending")


class PropertyOfferUpdateStateAPIViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.loggedInUser = UserFactory()
        self.client.force_authenticate(user=self.loggedInUser)
        self.image = PropertyImagesFactory()
        self.amenities = PropertyAmenityFactory()
        self.property = PropertyFactory(owner=self.loggedInUser)
        self.property_offer = PropertyOfferFactory(offered_by=self.user, property=self.property)
        self.url = reverse('update_state', kwargs={'pk': self.property_offer.id})

    @patch("communications.tasks.send_email_on_offer_state_update.delay")
    def test_update_offer_state_to_accepted(self, mock_send_email):
        data = {
            "state": MobileState.ACCEPTED
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.property_offer.refresh_from_db()
        self.assertEqual(self.property_offer.state, MobileState.ACCEPTED)
        self.assertEqual(mock_send_email.call_count, 1)
        mock_send_email.assert_called_with(self.property_offer.id)

    @patch("communications.tasks.send_email_on_offer_state_update.delay")
    def test_update_offer_state_to_rejected(self, mock_send_email):
        data = {
            "state": MobileState.REJECTED
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.property_offer.refresh_from_db()
        self.assertEqual(self.property_offer.state, MobileState.REJECTED)
        self.assertEqual(mock_send_email.call_count, 1)
        mock_send_email.assert_called_with(self.property_offer.id)