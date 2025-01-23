from django.db import models

from Finance.models import Department



class Staff(models.Model):
    StaffId = models.AutoField(primary_key=True, unique=True)
    StaffName = models.CharField(max_length=200)
    Role = models.CharField(max_length=200)
    Salary = models.IntegerField()
    DepartmentId = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    HireDate = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.DepartmentId:
            return f"{self.StaffName} - Role:{self.Role} - In:{self.DepartmentId.DepartmentName}"
        return f"{self.StaffName} - Role:{self.Role}"
