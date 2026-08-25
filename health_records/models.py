from django.db import models
from django.utils import timezone
from animals.models import Animal


class HealthRecord(models.Model):

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="health_records"
    )

    diagnosis = models.CharField(
        max_length=200
    )

    treatment = models.TextField()

    checkup_date = models.DateField(
    default=timezone.now
    )

    veterinarian = models.CharField(
        max_length=100
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.animal.name} - {self.checkup_date}"