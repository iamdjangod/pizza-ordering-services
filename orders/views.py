from rest_framework import viewsets
from rest_framework import exceptions

from orders.models import Order, OrderDetail
from orders.serializers import (
    OrderRetrieveSerializer,
    OrderCreateSerializer,
    OrderDetailCreateSerializer,
    OrderStatusRetrieveSerializer,
    OrderDetailUpdateSerializer,
    OrderStatusUpdateSerializer)


class OrderCreateListView(viewsets.ModelViewSet):
    """
    View to list all orders or create one.
    * no authentication is currently required
    """
    queryset = Order.objects.all()
    filter_fields = ('id', 'number', 'customer', 'status')

    def get_serializer_class(self):
        method = self.request.method
        serializer_class = OrderRetrieveSerializer
        if method == 'POST':
            serializer_class = OrderCreateSerializer
        return serializer_class

    def perform_create(self, serializer):
        """
        We need to override this method to add order details after a order
        is placed. Also note that extra validation is added to ensure order
        details come in the json data.
        """
        details = self.request.data.get('details')

        if not details:
            raise exceptions.ValidationError({
                'details': 'Please provide details for this order'
            })

        order_details_serialized = OrderDetailCreateSerializer(
            data=details, many=True)

        order_details_serialized.is_valid(raise_exception=True)

        order = serializer.save()
        order_details_serialized.save(order=order)


class OrderRetrieveDeleteView(viewsets.ModelViewSet):
    """
    View to get or delete a specific order details.
    * no authentication is currently required
    """
    serializer_class = OrderRetrieveSerializer
    queryset = Order.objects.all()


class OrderRetrieveUpdateStatusView(viewsets.ModelViewSet):
    """
    View to get or update a specific order details.
    * no authentication is currently required
    """

    queryset = Order.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        serializer_class = OrderStatusRetrieveSerializer
        if method == 'PUT':
            serializer_class = OrderStatusUpdateSerializer
        return serializer_class


class OrderDetailsUpdateView(viewsets.ModelViewSet):
    """
    View to update a specific order details.
    * no authentication is currently required
    """
    serializer_class = OrderDetailUpdateSerializer
    queryset = OrderDetail.objects.all()
