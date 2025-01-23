# Generated by Django 4.1.7 on 2025-01-23 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Inventory", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Supplier",
            fields=[
                (
                    "SupplierId",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("SupplierName", models.CharField(max_length=200)),
                ("ContactDetails", models.CharField(max_length=200)),
                ("Location", models.CharField(max_length=200)),
                ("ContractTerms", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                (
                    "PurchaseOrderId",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("TotalAmount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("OrderDate", models.DateField(auto_now_add=True)),
                ("DeliveryDate", models.DateField(blank=True, null=True)),
                ("OrderStatus", models.CharField(max_length=200)),
                (
                    "ProductId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Inventory.product",
                    ),
                ),
            ],
        ),
    ]
