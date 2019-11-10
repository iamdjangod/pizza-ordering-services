from rest_framework import serializers

from orders.models import Order, OrderDetail


class UniqueUpdateValidator(object):
    instance = None
    initial_data = {}

    def set_context(self, serializer):
        """
        Code from rest_framework/validators :joy:
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Personal touch to this method :)
        self.initial_data = getattr(serializer, 'initial_data', None)

    def __call__(self, attrs):
        """
        We will override this method to ensure the order details is unique for
        pizza and size, in the current request context.
        """
        unique_store = []
        for data in self.initial_data:
            to_validate = (data.get('pizza'), data.get('size'))
            if to_validate in unique_store:
                raise serializers.ValidationError({
                    'pizza': (
                        u'Already added a pizza with this size, '
                        u'consider using quantity'
                    )
                })
            unique_store.append(to_validate)


class UniqueUpdateDBValidator(object):
    instance = None
    initial_data = {}

    def set_context(self, serializer):
        """
        Code from rest_framework/validators
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, 'instance', None)
        # Personal touch to this method :)
        self.initial_data = getattr(serializer, 'initial_data', None)

    def __call__(self, attrs):
        """
        Validate we are not updating a order detail that matches another
        order detail from the same order, in that case we should update
        the quantity from the original order detail.
        """
        data = self.initial_data
        qs = OrderDetail.objects.filter(
            order=self.instance.order,
            pizza=data.get('pizza'),
            size=data.get('size')
        ).exclude(id=self.instance.id).exists()

        if qs:
            raise serializers.ValidationError({
                'pizza': (
                    u'Looks like this order already has this '
                    u'pizza and size.'
                )
            })


class UniqueUpdateStatusValidator(object):
    instance = None
    status_not_permited = [
        Order.OUT_FOR_DELIVERY,
        Order.DELIVERED,
        Order.RETURNED
    ]

    def set_context(self, serializer):
        """
        Code from rest_framework/validators
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, 'instance', None)

    def __call__(self, attrs):
        """
        Validate we are not updating a order detail that matches another
        order detail from the same order, in that case we should update
        the quantity from the original order detail.
        """
        order = self.instance.order
        if order.status in self.status_not_permited:
            raise serializers.ValidationError({
                (
                    u'This order is `{status}` and cannot be '
                    u'updated at this moment'
                ).format(
                    status=order.get_status_display()
                )
            })
