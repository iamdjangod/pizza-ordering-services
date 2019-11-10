from django.db import models


class Pizza(models.Model):
    name = models.CharField(
        u'Name',
        max_length=128
    )
    description = models.TextField(
        u'Description',
        blank=True
    )

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return u'{id} - {name}'.format(
            id=self.id,
            name=self.name
        )
