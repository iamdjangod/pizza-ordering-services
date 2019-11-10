from django.db import models


class Customer(models.Model):
    first_name = models.CharField(
        u'First name',
        max_length=128
    )
    last_name = models.CharField(
        u'Last name',
        max_length=128,
        blank=True
    )
    email = models.EmailField(
        u'Email',
        blank=True
    )
    phone = models.CharField(
        u'Phone',
        max_length=16,
        unique=True,
        help_text=u'Phone for rider to contact'
    )
    address = models.TextField(
        u'Address',
        help_text=u'Address for pizza delivery'
    )

    class Meta:
        ordering = (
            'first_name',
            'last_name',
        )

    def __str__(self):
        return u'{full_name} - [{email} - {phone}]'.format(
            full_name=self.full_name,
            email=self.email,
            phone=self.phone
        )
    
    @property
    def full_name(self):
        return u'{first_name} {last_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name
        )
