from django.db import models
from Sales.models import *
from HR.models import *
from Inventory.models import *
from Procurement.models import *


class Store(models.Model):
    StoreId = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    ManagerId = models.OneToOneField(
        Employee,
        unique=True,
        on_delete=models.DO_NOTHING,
        primary_key=True,
    )