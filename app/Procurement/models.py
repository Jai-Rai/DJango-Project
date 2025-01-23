from django.db import models
from Inventory.models import Product
<<<<<<< Updated upstream
=======
from django.db.models import Sum, Avg, Count
from datetime import datetime, timedelta
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
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
=======
        Retrieves all products associated with the supplier.
        """
        return Product.objects.filter(SupplierId=self.SupplierId)

    def SetSupplierData(self, **kwargs):
        """
        Updates the supplier's data.
        :param kwargs: Dictionary of field names and their new values.
        """
        allowed_fields = {"SupplierName", "ContactDetails", "Location", "ContractTerms"}
        for field, value in kwargs.items():
            if field not in allowed_fields:
                raise ValueError(f"Invalid field: {field}")
            setattr(self, field, value)
        self.save()

    def ViewSupplierPerformance(self, dateRange=30):
        """
        Analyses the supplier's performance based on delivered orders over a specified period.
        :param dateRange: The number of days to consider for the analysis.
        :return: Performance metrics.
        """
        endDate = datetime.now()
        startDate = endDate - timedelta(days=dateRange)

        orders = PurchaseOrder.objects.filter(
            ProductId__SupplierId=self.SupplierId,
            DeliveryDate__range=[startDate, endDate],
            OrderStatus="Delivered",
        )

        totalAmount = orders.aggregate(total=Sum("TotalAmount"))["total"] or 0
        totalOrders = orders.count()

        performance = {
            "TotalDeliveredOrders": totalOrders,
            "TotalDeliveredAmount": totalAmount,
            "AverageOrderValue": totalAmount / totalOrders if totalOrders > 0 else 0,
        }
        return performance
>>>>>>> Stashed changes


class PurchaseOrder(models.Model):
    PurchaseOrderId = models.AutoField(primary_key=True, unique=True)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    OrderDate = models.DateField(auto_now_add=True)
    DeliveryDate = models.DateField()
    OrderStatus = models.CharField(max_length=200)

    def __str__(self):
<<<<<<< Updated upstream
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
=======
        return f"Id:{self.PurchaseOrderId} - Contains:{self.ProductId.ProductName} - Amount:{self.TotalAmount} - Status:{self.OrderStatus}"

    @classmethod
    def CreatePurchaseOrder(
        cls, product, totalAmount, deliveryDate, orderStatus="Pending"
    ):
        """
        Creates a new purchase order.
        :param product: Product instance to be ordered.
        :param totalAmount: Total amount of the purchase.
        :param deliveryDate: Expected delivery date.
        :param orderStatus: Status of the order. Default is 'Pending'.
        """
        return cls.objects.create(
            ProductId=product,
            TotalAmount=totalAmount,
            DeliveryDate=deliveryDate,
            OrderStatus=orderStatus,
>>>>>>> Stashed changes
        )

    def GetPurchaseOrderStatus(self):
        """
<<<<<<< Updated upstream
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
=======
        Retrieves the current status of the purchase order.
        """
        return self.OrderStatus

    def SetPurchaseOrder(self, **kwargs):
        """
        Updates the purchase order's details.
        :param kwargs: Dictionary of field names and their new values.
        """
        allowed_fields = {"TotalAmount", "DeliveryDate", "OrderStatus"}
        for field, value in kwargs.items():
            if field not in allowed_fields:
                raise ValueError(f"Invalid field: {field}")
            setattr(self, field, value)
        self.save()
>>>>>>> Stashed changes
