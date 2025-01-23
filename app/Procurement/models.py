from django.db import models
from Inventory.models import Product


class Supplier(models.Model):
    SupplierId = models.AutoField(primary_key=True, unique=True)
    SupplierName = models.CharField(max_length=200)
    ContactDetails = models.CharField(max_length=200)
    Location = models.CharField(max_length=200)
    ContractTerms = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.SupplierName} - {self.Location}"
    

class PurchaseOrder(models.Model):
    PurchaseOrderId = models.AutoField(primary_key=True, unique=True)
    TotalAmount = models.IntegerField()
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    OrderDate = models.DateField(auto_now_add=True)
    DeliveryDate = models.DateField()
    OrderStatus = models.CharField(max_length=200)
    
    def CreatePurchaseOrder():
        PurchaseOrder.objects.create()

    def __str__(self):
        return f"Id:{self.PurchaseOrderId} - Conatins:{self.ProductId.ProductName} - Amount:{self.TotalAmount} - Status{self.OrderStatus}"
