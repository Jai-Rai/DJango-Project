from django.db import models
from Sales.models import *
from Inventory.models import *
from Finance.models import *
from Procurement.models import *

class Employee(models.Model):
    EmployeeId = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    ManagerId = models.ForeignKey(Store, on_delete=models.DO_NOTHING)