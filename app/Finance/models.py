from django.db import models


class Department(models.Model):
    DepartmentId = models.AutoField(primary_key=True, unique=True)
    DepartmentName = models.CharField(max_length=200)
    ManagerId = models.OneToOneField(
        "HR.Staff", on_delete=models.SET_NULL, null=True, blank=True
    )
    Budget = models.IntegerField()

    def __str__(self):
        if self.ManagerId:
            return f"{self.DepartmentName} - Manager:{self.ManagerId.StaffName} "
        return f"{self.DepartmentName} "
