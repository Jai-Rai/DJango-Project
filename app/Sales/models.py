from django.db import models
from Inventory.models import Store
from HR.models import Staff


class Sales(models.Model):
    SalesId = models.AutoField(primary_key=True, unique=True)
    PaymentMethod = models.CharField(max_length=200)
    TotalAmount = models.CharField(max_length=15)
    StoreId = models.ForeignKey(Store, on_delete=models.CASCADE)
    StaffId = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    DateOfSale = models.DateField(auto_now_add=True)
