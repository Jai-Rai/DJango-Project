from django.db import models
from Inventory.models import Product



class Supplier(models.Model):
    SupplierId = models.AutoField(primary_key=True, unique=True)
    SupplierName = models.CharField(max_length=200)
    ContactDetails = models.CharField(max_length=200)
    Location = models.CharField(max_length=200)
    ContractTerms = models.CharField(max_length=200)


class PurchaseOrder(models.Model):
    PurchaseOrderId = models.AutoField(primary_key=True, unique=True)
    TotalAmount = models.CharField(max_length=15)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    OrderDate = models.DateField(auto_now_add=True)
    DeliveryDate = models.DateField()
    OrderStatus = models.CharField()
