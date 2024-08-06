from django.urls import reverse
from django.core import mail

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
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
        self.property_owner = UserFactory()
        self.image = PropertyImagesFactory()
        self.amenities = PropertyAmenityFactory()
        self.property = PropertyFactory(owner=self.property_owner)
        self.base_url = reverse("create_offer_generic_api")

    def test_create_offer(self):
        data = {
            "price": 500000,
            "property": self.property.id,
            "is_active": True,
            "state": "pending"
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PropertyOffers.objects.count(), 1)
        offer = PropertyOffers.objects.get()
        self.assertEqual(offer.price, 500000)
        self.assertEqual(offer.offered_by, self.user)
        self.assertEqual(offer.property, self.property)
        self.assertEqual(offer.is_active, True)
        self.assertEqual(offer.state, "pending")

    def test_create_offer_without_property_id(self):
        data = {
            "price": 500000,
            "property": None,
            "is_active": True,
            "state": "pending"
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_offer_with_invalid_property_id(self):
        data = {
            "price": 500000,
            "property": 25,
            "is_active": True,
            "state": "pending"
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_offer_by_property_owner(self):
        self.client.force_authenticate(self.property_owner)
        data = {
            "price": 500000,
            "property": self.property.id,
            "is_active": True,
            "state": "pending"
        }
        response = self.client.post(self.base_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data,
            {"detail": ErrorDetail(string="You do not have permission to perform this action.",
                                   code="permission_denied")}
        )


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
        self.url = reverse("update_state", kwargs={"pk": self.property_offer.id})

    @patch("communications.tasks.send_email_on_offer_state_update.delay")
    def test_update_offer_state_to_accepted(self, mock_send_email):
        data = {
            "state": MobileState.ACCEPTED
        }
        response = self.client.patch(self.url, data, format="json")
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
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.property_offer.refresh_from_db()
        self.assertEqual(self.property_offer.state, MobileState.REJECTED)
        self.assertEqual(mock_send_email.call_count, 1)
        mock_send_email.assert_called_with(self.property_offer.id)

    @patch("communications.tasks.send_email_on_offer_state_update.delay")
    def test_update_offer_state_by_unauthorized_user(self, mock_send_email=None):
        self.client.force_authenticate(self.user)
        data = {
            "state": MobileState.ACCEPTED
        }
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.property_offer.refresh_from_db()
        self.assertEqual(self.property_offer.state, MobileState.REJECTED)
        self.assertEqual(mock_send_email.call_count, 0)
