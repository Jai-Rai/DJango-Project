from django.db import models
from Inventory.models import *
from HR.models import *
from Finance.models import *
from Procurement.models import *


class Sales(models.Model):
    SalesId = models.AutoField(primary_key=True, unique=True)
    PaymentMethod = models.CharField(max_length=200)
    TotalAmount = models.CharField(max_length=15)
    StoreId = models.ForeignKey(Store, on_delete=models.CASCADE)
    StaffId = models.ForeignKey(Staff, on_delete=models.SET_NULL)
    DateOfSale = models.DateField(auto_now_add=True)
