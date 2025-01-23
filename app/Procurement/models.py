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

    def GetSupplierProducts(self):
        """
        Returns all products supplied by this supplier.
        """
        return Product.objects.filter(SupplierId=self).values("ProductName", "Category", "Price")

    def SetSupplierData(self, SupplierName=None, ContactDetails=None, Location=None, ContractTerms=None):
        """
        Updates supplier details.
        """
        if SupplierName:
            self.SupplierName = SupplierName
        if ContactDetails:
            self.ContactDetails = ContactDetails
        if Location:
            self.Location = Location
        if ContractTerms:
            self.ContractTerms = ContractTerms
        self.save()

    def ViewSupplierPerformance(self):
        """
        Placeholder for supplier performance metrics. This could include delivery timelines, order accuracy, etc.
        """
        # Example performance metric: Count of products supplied
        total_products = Product.objects.filter(SupplierId=self).count()
        return {
            "TotalProducts": total_products,
            "SupplierName": self.SupplierName,
            "Location": self.Location,
        }


class PurchaseOrder(models.Model):
    PurchaseOrderId = models.AutoField(primary_key=True, unique=True)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    OrderDate = models.DateField(auto_now_add=True)
    DeliveryDate = models.DateField()
    OrderStatus = models.CharField(max_length=200)

    def __str__(self):
        return f"Id: {self.PurchaseOrderId} - Contains: {self.ProductId.ProductName} - Amount: {self.TotalAmount} - Status: {self.OrderStatus}"

    @staticmethod
    def CreatePurchaseOrder(product, total_amount, delivery_date, status="Pending"):
        """
        Creates a new purchase order.
        :param product: Product instance to associate with the order.
        :param total_amount: Total amount for the order.
        :param delivery_date: Expected delivery date.
        :param status: Initial status of the order (default is "Pending").
        """
        if not isinstance(product, Product):
            raise ValueError("Invalid product instance.")
        return PurchaseOrder.objects.create(
            ProductId=product, TotalAmount=total_amount, DeliveryDate=delivery_date, OrderStatus=status
        )

    def GetPurchaseOrderStatus(self):
        """
        Returns the current status of the purchase order.
        """
        return self.OrderStatus

    def SetPurchaseOrder(self, TotalAmount=None, DeliveryDate=None, OrderStatus=None):
        """
        Updates the purchase order details.
        """
        if TotalAmount:
            self.TotalAmount = TotalAmount
        if DeliveryDate:
            self.DeliveryDate = DeliveryDate
        if OrderStatus:
            self.OrderStatus = OrderStatus
        self.save()