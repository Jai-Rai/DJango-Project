from django.db import models

from Inventory.models import Store


class Staff(models.Model):
    StaffId = models.AutoField(primary_key=True, unique=True)
    StaffName = models.CharField(max_length=200)
    Role = models.CharField(max_length=200)
    Salary = models.CharField(max_length=15)
    DepartmentId = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True) 
    HireDate = models.DateField(auto_now_add=True)
