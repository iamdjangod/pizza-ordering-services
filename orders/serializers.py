from rest_framework import serializers
from customers.serializers import CustomerSerializer
from orders.models import Order, OrderDetail
from orders.validators import (
    UniqueUpdateValidator,
    UniqueUpdateDBValidator,
    UniqueUpdateStatusValidator
)
from pizzas.serializers import PizzaSerializer


class OrderDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'pizza',
            'size',
            'quantity',
            'customer_details'
        )
        read_only_fields = ('order',)
        validators = [
            UniqueUpdateValidator()
        ]


class OrderDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'pizza',
            'size',
            'quantity',
            'customer_details'
        )
    validators = [
        UniqueUpdateStatusValidator(),
        UniqueUpdateDBValidator()
    ]


class OrderDetailRetrieveSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer()
    size = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'pizza',
            'size',
            'quantity',
            'customer_details'
        )

    def get_size(self, obj):
        return obj.get_size_display()


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'number',
            'customer',
            'status'
        )

    def get_status(self, obj):
        return obj.get_status_display()


class OrderRetrieveSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    details = OrderDetailRetrieveSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'number',
            'customer',
            'status',
            'details'
        )

    def get_status(self, obj):
        return obj.get_status_display()


class OrderStatusRetrieveSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'status',
        )

    def get_status(self, obj):
        return obj.get_status_display()


class OrderStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'id',
            'status',
        )
