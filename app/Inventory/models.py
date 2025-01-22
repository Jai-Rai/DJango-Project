from django.db import models
from Sales.models import *
from HR.models import *
from Finance.models import *
from Procurement.models import *


class Product(models.Model):
    ProductId = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_level = models.IntegerField()
    reorder_level = models.IntegerField()
    last_purchase_date = models.DateField(null=True, blank=True)


class Store(models.Model):
    StoreId = models.AutoField(primary_key=True, unique=True)
    StoreName = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    ContactNumber = models.CharField(max_length=15)
    ManagerId = models.OneToOneField(
        Employee,
        unique=True,
        on_delete=models.DO_NOTHING,
        primary_key=True,
    )
    TotalSales = models.IntegerField()
    OperatingHours = models.IntegerField()


class StockLocation(models.Model):
    StockLocationId = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
