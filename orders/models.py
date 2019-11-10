from django.db import models

from customers.models import Customer
from pizzas.models import Pizza


class Order(models.Model):
    RECEIVED = 1
    IN_PROCESS = 2
    OUT_FOR_DELIVERY = 3
    DELIVERED = 4
    # Status 5 is for some special cases where product wasn't delivered or customer not satisfied with product.
    RETURNED = 5

    ORDER_STATUSES = (
        (RECEIVED, u'Received'),
        (IN_PROCESS, u'In Process'),
        (OUT_FOR_DELIVERY, u'Out For Delivery'),
        (DELIVERED, u'Delivered'),
        (RETURNED, u'Returned')
    )
    number = models.CharField(
        u'Order #',
        max_length=256,
        unique=True
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
    )
    status = models.PositiveSmallIntegerField(
        choices=ORDER_STATUSES,
        default=1
    )


class OrderDetail(models.Model):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    EXTRA_LARGE = 4

    PIZZA_SIZE = (
        (SMALL, u'Small'),
        (MEDIUM, u'Medium'),
        (LARGE, u'Large'),
        (EXTRA_LARGE, u'Extra Large'),
    )

    order = models.ForeignKey(
        Order,
        verbose_name=u'Order #',
        on_delete=models.CASCADE,
        related_name=u'details'
    )
    pizza = models.ForeignKey(
        Pizza,
        verbose_name=u'Pizza',
        on_delete=models.DO_NOTHING,
    )
    size = models.PositiveSmallIntegerField(
        u'Size',
        choices=PIZZA_SIZE
    )
    quantity = models.PositiveIntegerField(
        u'quantity',
        default=1
    )
    customer_details = models.TextField(
        u'Details',
        blank=True
    )

    class Meta:
        ordering = ('-pk', )
        unique_together = ('order', 'pizza', 'size',)
