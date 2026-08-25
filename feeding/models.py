from django.db import models
from animals.models import Animal


class FeedingSchedule(models.Model):

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="feeding_schedules"
    )

    feeding_date = models.DateField()

    feeding_time = models.TimeField()

    food = models.CharField(
        max_length=200
    )

    quantity = models.CharField(
        max_length=100
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.animal.name} - {self.feeding_date} - {self.feeding_time}"