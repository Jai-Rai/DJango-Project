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

    def GetStocklevel(self):
        return self.stock_amount

    def SetReorderLevel(self, NewLevel):
        """Sets new reorder level"""
        if NewLevel is int:
            self.order_limit = NewLevel
            return True
        return False

    def TransferStock(self, StoreId, quantity):
        StockLocation.objects.create(
            Product=self,
            StoretoreId=StoreId,
            Quantity=quantity,
            Date=models.DateField(auto_now=True),
        )

    def __str__(self):
        return f"{self.ProductName} - Level:{self.StockLevel} Order at:{self.ReorderLevel}"


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

    def get_all_products(self):
        """
        Retrieves all products associated with this store.
        Returns QuerySet of products with their details.
        """
        try:
            # try getting all products with this stores id
            return (
                StockLocation.objects.filter(StoreId = '')
            )
        except Exception as e:
            raise ValueError(f"Error retrieving products: {str(e)}")

    def view_store_performance(self, date_range=30):
        """
        Analyzes store performance metrics over a specified period.
        Args:
            date_range (int): Number of days to analyze (default: 30)
        Returns:
            dict: Performance metrics including sales, average daily revenue, etc.
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=date_range)

            # Assuming you have an Order/Sale model with appropriate relations
            sales_data = self.dd.filter(
                date__range=[start_date, end_date]
            ).aaggregate(
                total_sales=Sum("total_amount"),
                average_daily_sales=Avg("total_amount"),
                total_orders=models.Count("id"),
            )

            # Calculate additional metrics
            performance_metrics = {
                "period_total_sales": sales_data["total_sales"] or 0,
                "average_daily_sales": sales_data["average_daily_sales"] or 0,
                "total_orders": sales_data["total_orders"] or 0,
                "store_efficiency": (sales_data["total_sales"] or 0)
                / self.OperatingHours,
                "sales_per_hour": (sales_data["total_sales"] or 0)
                / (self.OperatingHours * date_range),
            }

            return performance_metrics

        except Exception as e:
            raise ValueError(f"Error calculating store performance: {str(e)}")

    def edit_store_data(self, **kwargs):
        """
        Updates store information with provided data.
        Args:
            **kwargs: Dictionary of fields to update and their new values
        Returns:
            bool: True if update successful, raises exception otherwise
        """
        try:
            valid_fields = {
                "StoreName",
                "Location",
                "ContactNumber",
                "ManagerId",
                "OperatingHours",
            }
            # Filter out invalid fields
            update_data = {k: v for k, v in kwargs.items() if k in valid_fields}
            if not update_data:
                raise ValidationError("No valid fields provided for update")

            # Validate contact number format if it's being updated
            if "ContactNumber" in update_data:
                if not update_data["ContactNumber"].replace("+", "").isdigit():
                    raise ValidationError("Invalid contact number format")

            # Validate operating hours if being updated
            if "OperatingHours" in update_data:
                if not 0 < update_data["OperatingHours"] <= 24:
                    raise ValidationError("Operating hours must be between 1 and 24")

            # Update the fields
            for field, value in update_data.items():
                setattr(self, field, value)
            self.full_clean()  # Validate all fields
            self.save()
            return True

        except ValidationError as ve:
            raise ValidationError(f"Validation error: {str(ve)}")
        except Exception as e:
            raise ValueError(f"Error updating store data: {str(e)}")

    def __str__(self):
        return f"{self.StoreName} - {self.Location}"


class StockLocation(models.Model):
    StockLocationId = models.AutoField(primary_key=True, unique=True)
    ProductId = models.ForeignKey(Product, on_delete=models.CASCADE)
    StoreId = models.ForeignKey(Store, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.ProductId.ProductName} - {self.StoreId.StoreName} - Amount: {self.Quantity}"
        )