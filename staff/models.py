from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):

    DESIGNATION_CHOICES = [
        ("Zoo Keeper", "Zoo Keeper"),
        ("Veterinarian", "Veterinarian"),
        ("Receptionist", "Receptionist"),
        ("Security", "Security"),
        ("Cleaner", "Cleaner"),
        ("Manager", "Manager"),
    ]

    DEPARTMENT_CHOICES = [
        ("Animal Care", "Animal Care"),
        ("Medical", "Medical"),
        ("Administration", "Administration"),
        ("Security", "Security"),
        ("Maintenance", "Maintenance"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    designation = models.CharField(
        max_length=50,
        choices=DESIGNATION_CHOICES
    )

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class LeaveRequest(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="leave_requests"
    )

    leave_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.staff} - {self.leave_date} - {self.status}"