from django.db import models
from Sales.models import *
from HR.models import *
from Finance.models import *
from Procurement.models import *


class Product(models.Model):
    ProductId = models.AutoField(primary_key=True, unique=True)
    ProductName = models.CharField(max_length=200)
    Category = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    StockLevel = models.IntegerField()
    ReorderLevel = models.IntegerField()
    LastPurchaseDate = models.DateField(null=True, blank=True)
    SupplierId = models.ForeignKey(
        Supplier,
        null=True,
        on_delete=models.SET_NULL,
        primary_key=True,
    )


class Store(models.Model):
    StoreId = models.AutoField(primary_key=True, unique=True)
    StoreName = models.CharField(max_length=200)
    Location = models.CharField(max_length=200)
    ContactNumber = models.CharField(max_length=15)
    ManagerId = models.OneToOneField(
        Staff,
        null=True,
        on_delete=models.SET_NULL,
        primary_key=True,
    )
    TotalSales = models.IntegerField()
    OperatingHours = models.IntegerField()


class StockLocation(models.Model):
    StockLocationId = models.ForeignKey(Product, on_delete=models.CASCADE)
    StoreId = models.ForeignKey(Store, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Date = models.DateTimeField(auto_now_add=True)
