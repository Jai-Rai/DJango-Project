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
        related_name='staff'  # Ensure related_name is added
    )
    HireDate = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.DepartmentId:
            return f"{self.StaffName} - Role: {self.Role} - In: {self.DepartmentId.DepartmentName}"
        return f"{self.StaffName} - Role: {self.Role}"

    def GetStaffData(self):
        """
        Returns the staff member's data as a dictionary.
        """
        return {
            "StaffId": self.StaffId,
            "StaffName": self.StaffName,
            "Role": self.Role,
            "Salary": self.Salary,
            "Department": self.DepartmentId.DepartmentName if self.DepartmentId else None,
            "HireDate": self.HireDate,
        }

    def EditStaffData(self, StaffName=None, Role=None, Salary=None):
        """
        Edits the staff member's data.
        :param StaffName: New name for the staff member.
        :param Role: New role for the staff member.
        :param Salary: New salary for the staff member.
        """
        if StaffName:
            self.StaffName = StaffName
        if Role:
            self.Role = Role
        if Salary and isinstance(Salary, int) and Salary >= 0:
            self.Salary = Salary
        elif Salary is not None:
            raise ValueError("Salary must be a non-negative integer.")
        self.save()

    def ViewPerformance(self):
        """
        Placeholder for viewing staff performance. Returns a string for now.
        This would typically integrate with a performance tracking system.
        """
        return f"Performance data for {self.StaffName} is not yet implemented."

    def AssignDepartment(self, DepartmentId):
        """
        Assigns the staff member to a department.
        :param DepartmentId: The department instance to assign.
        """
        if isinstance(DepartmentId, Department):
            self.DepartmentId = DepartmentId
            self.save()
        else:
            raise ValueError("Invalid department instance.")