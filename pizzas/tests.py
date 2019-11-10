from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pizzas.models import Pizza
from pizzas.serializers import PizzaSerializer


class PizzaTests(APITestCase):

    def test_create_pizza_success(self):
        """
        To create a new pizza.
        """
        url = reverse('pizzas:create-list-pizzas')
        data = {
            'name': 'Pepperoni',
            'description': 'Delicious',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pizza.objects.count(), 1)
        self.assertEqual(Pizza.objects.get().name, 'Pepperoni')

    def test_create_pizza_error(self):
        """
        To validate the data received.
        """
        url = reverse('pizzas:create-list-pizzas')
        data = {
            'name': '',
            'description': '',
        }

        response = self.client.post(url, data, format='json')

        serialized_data = PizzaSerializer(data=data)

        self.assertFalse(serialized_data.is_valid())
        self.assertJSONEqual(
            response.content, serialized_data.errors)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Pizza.objects.count(), 0)
