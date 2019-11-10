from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer
from orders.models import Order
from pizzas.models import Pizza


class OrderTests(APITestCase):
    ORDER_FIELDS_VALIDATION = '''{
        "number":["This field may not be blank."],
        "customer":["This field may not be null."]
    }'''

    ORDER_DETAILS_MISSING_VALIDATION = '''{
        "details":"Please provide details for this order"
    }'''

    ORDER_DETAILS_FIELDS_VALIDATION = '''
    [{
        "pizza":["This field may not be null."],
        "size":["\\"100\\" is not a valid choice."]
    }]
    '''

    ORDER_DETAILS_DUPLICATE_VALIDATION = '''
    [{
        "pizza":["Already added a pizza with this size, consider using quantity"]},
        {"pizza":["Already added a pizza with this size, consider using quantity"]
    }]
    '''

    def setUp(self):
        Customer.objects.create(
            first_name='Test',
            email='customer@mail.com',
            address='address'
        )

        Pizza.objects.create(
            name='Pepperoni'
        )

    def test_create_order_success(self):
        """
        To create a new order.
        """
        url = reverse('orders:create-list-orders')
        data = {
            'customer': 1,
            'number': '1',
            'details': [
                {
                    'pizza': 1,
                    'size': 1
                }
            ]
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().customer.id, 1)
        self.assertIsNotNone(Order.objects.get().details)

    def test_create_order_error(self):
        """
        To validate data we receive for the order.
        """
        url = reverse('orders:create-list-orders')
        data = {
            'customer': '',
            'number': '',
            'details': []
        }

        response = self.client.post(url, data, format='json')

        self.assertJSONEqual(
            response.content, self.ORDER_FIELDS_VALIDATION)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_detail_missing_error(self):
        """
        To validate data we receive for the order detail.
        """
        url = reverse('orders:create-list-orders')
        data = {
            'customer': 1,
            'number': '1',
            'details': [

            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertJSONEqual(
            response.content, self.ORDER_DETAILS_MISSING_VALIDATION)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_detail_error(self):
        """
        To validate data we receive for the order detail.
        """
        url = reverse('orders:create-list-orders')
        data = {
            'customer': 1,
            'number': '1',
            'details': [
                {
                    'pizza': '',
                    'size': '100'
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertJSONEqual(
            response.content, self.ORDER_DETAILS_FIELDS_VALIDATION)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_detail_duplicate_error(self):
        """
        To validate data we receive for the order detail.
        """
        url = reverse('orders:create-list-orders')
        data = {
            'customer': 1,
            'number': '1',
            'details': [
                {
                    'pizza': '1',
                    'size': '1'
                },
                {
                    'pizza': '1',
                    'size': '1'
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertJSONEqual(
            response.content, self.ORDER_DETAILS_DUPLICATE_VALIDATION)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
