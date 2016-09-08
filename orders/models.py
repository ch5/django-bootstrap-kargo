from __future__ import unicode_literals

import uuid as uuid

from django.db import models
from decimal import Decimal

# every Django model fields can be customized by re-use parameter under
# simple dictionary format
AMOUNT_MONEY = {
                'max_digits': 25, 'decimal_places': 2,
                'default': Decimal('0.00')
               }

class CommonInfo(models.Model):
    """
    Abstract models contains mandatory fields on each models.
    Every class can have these fields by instantiate from this class.
    """
    remarks = models.TextField(blank=True, verbose_name='Keterangan Tambahan')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Dibuat')
    modified = models.DateTimeField(auto_now=True, verbose_name='Waktu diedit')
    status = models.BooleanField(default=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    # flag for update, delete, sync and coming from cloud
    is_delete = models.BooleanField(default=False, verbose_name='Soft Delete')

    class Meta:
        abstract = True


class ODOrder(CommonInfo):
    """
    Order details contain name, phone and amount of total price order
    """
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    price = models.DecimalField(**AMOUNT_MONEY)

    def __unicode__(self):
        return '{}'.format(self.user.username)

    class Meta:
        verbose_name_plural = "Customer"

# New module vehicle
class Vehicle(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name="Nama Angkutan")
    driver = models.CharField(max_length=50, verbose_name="Pengemudi")
    number = models.CharField(max_length=50, verbose_name="Nomer Angkutan")
    capacity = models.PositiveIntegerField(verbose_name="Kapasitas")

    def __unicode__(self):
        return self.number
