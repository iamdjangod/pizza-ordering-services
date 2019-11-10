from rest_framework import viewsets

from pizzas.models import Pizza
from pizzas.serializers import PizzaSerializer


class PizzaCreateListView(viewsets.ModelViewSet):
    """
    View to list all pizzas or create one.
    * no authentication is currently required
    """
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()
    filter_fields = ('id', 'name', )


class PizzaUpdateView(viewsets.ModelViewSet):
    """
    View to update pizzas.
    * no authentication is currently required
    """
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()
