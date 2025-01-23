from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum, Avg
from datetime import datetime, timedelta

class Product(models.Model):
    ProductId = models.AutoField(primary_key=True, unique=True)
    ProductName = models.CharField(max_length=200)
    Category = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    StockLevel = models.IntegerField()
    ReorderLevel = models.IntegerField()
    LastPurchaseDate = models.DateField(null=True, blank=True)
    SupplierId = models.ForeignKey(
        "Procurement.Supplier",
        null=True,
        related_name="Supplier",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.ProductName} - Level:{self.StockLevel} Order at:{self.ReorderLevel}"

    def GetAllStores(self):
        """
        Returns all stores that stock this product.
        """
        return self.stocklocation_set.values("StoreId__StoreName", "StoreId__Location")

    def GetStockLevel(self):
        """
        Returns the total stock level for this product across all stores.
        """
        return self.stocklocation_set.aggregate(TotalStock=Sum("Quantity"))["TotalStock"] or 0

    def TransferStock(self, from_store, to_store, quantity):
        """
        Transfers stock of this product between stores.
        :param from_store: Store instance to transfer from.
        :param to_store: Store instance to transfer to.
        :param quantity: Quantity of stock to transfer.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        from_stock = self.stocklocation_set.filter(StoreId=from_store).first()
        to_stock = self.stocklocation_set.filter(StoreId=to_store).first()

        if not from_stock or from_stock.Quantity < quantity:
            raise ValidationError("Insufficient stock in the source store.")

        from_stock.Quantity -= quantity
        from_stock.save()

        if to_stock:
            to_stock.Quantity += quantity
        else:
            StockLocation.objects.create(ProductId=self, StoreId=to_store, Quantity=quantity)
        to_stock.save()

    def EditReorderLevel(self, new_reorder_level):
        """
        Updates the reorder level for this product.
        :param new_reorder_level: New reorder level (integer).
        """
        if new_reorder_level < 0:
            raise ValueError("Reorder level must be a non-negative integer.")
        self.ReorderLevel = new_reorder_level
        self.save()


class Store(models.Model):
    StoreId = models.AutoField(primary_key=True, unique=True)
    StoreName = models.CharField(max_length=200)
    Location = models.CharField(max_length=200)
    ContactNumber = models.CharField(max_length=15)
    ManagerId = models.OneToOneField(
        "HR.Staff",
        null=True,
        on_delete=models.SET_NULL,
    )
    TotalSales = models.IntegerField()
    OperatingHours = models.IntegerField()

    def __str__(self):
        return f"{self.StoreName} - {self.Location}"

    def GetAllProducts(self):
        """
        Returns all products stocked in this store.
        """
        return self.stocklocation_set.values("ProductId__ProductName", "Quantity")

    def ViewStorePerformance(self):
        """
        Returns the store's performance metrics.
        """
        return {
            "TotalSales": self.TotalSales,
            "AverageSalesPerHour": self.TotalSales / self.OperatingHours if self.OperatingHours else 0,
        }

    def EditStoreData(self, StoreName=None, Location=None, ContactNumber=None):
        """
        Updates the store's data.
        """
        if StoreName:
            self.StoreName = StoreName
        if Location:
            self.Location = Location
        if ContactNumber:
            self.ContactNumber = ContactNumber
        self.save()


class StockLocation(models.Model):
    StockLocationId = models.AutoField(primary_key=True, unique=True)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocklocation_set')
    StoreId = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stocklocation_set')
    Quantity = models.IntegerField()
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.ProductId.ProductName} - {self.StoreId.StoreName} - Amount: {self.Quantity}"
        )

    def AdjustStock(self, quantity):
        """
        Adjusts the stock quantity for this stock location.
        :param quantity: Positive to increase stock, negative to decrease stock.
        """
        if self.Quantity + quantity < 0:
            raise ValidationError("Insufficient stock for the operation.")
        self.Quantity += quantity
        self.save()

    def TransferStock(self, to_store, quantity):
        """
        Transfers stock from this location to another store.
        :param to_store: Store instance to transfer stock to.
        :param quantity: Quantity to transfer.
        """
        if quantity <= 0:
            raise ValueError("Transfer quantity must be positive.")

        if self.Quantity < quantity:
            raise ValidationError("Insufficient stock for transfer.")

        self.Quantity -= quantity
        self.save()

        to_stock_location, created = StockLocation.objects.get_or_create(
            ProductId=self.ProductId, StoreId=to_store,
            defaults={"Quantity": 0}
        )

        to_stock_location.Quantity += quantity
        to_stock_location.save()
