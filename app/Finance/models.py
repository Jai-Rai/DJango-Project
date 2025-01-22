from django.db import models
from HR.models import Staff


class Department(models.Model):
    DepartmentId = models.AutoField(primary_key=True, unique=True)
    DepartmentName = models.CharField(max_length=200)
    ManagerId = models.OneToOneField(
        Staff,
        on_delete=models.DO_NOTHING,
        primary_key=True,
    )
    Budget = models.IntegerField()