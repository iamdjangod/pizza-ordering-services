from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from customers.serializers import CustomerSerializer


class CustomerTests(APITestCase):

    def test_create_customer_success(self):
        """
        To create a new customer.
        """
        url = reverse('customers:create-list-customers')
        data = {
            'first_name': 'Test',
            'last_name': 'Customer',
            'phone': '08111306490',
            'address': 'Lagos',
            'email': 'testcustomer@mail.com'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().full_name, 'Test Customer')

    def test_create_customer_error(self):
        """
        To validate the data received.
        """
        url = reverse('customers:create-list-customers')
        data = {
            'first_name': '',
            'last_name': '',
            'phone': '',
            'address': '',
            'email': ''
        }

        serialized_data = CustomerSerializer(data=data)

        response = self.client.post(url, data, format='json')

        self.assertFalse(serialized_data.is_valid())
        self.assertJSONEqual(
            response.content, serialized_data.errors)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 0)
