from django.db import models
from staff.models import Staff


class Animal(models.Model):

    CATEGORY_CHOICES = [
        ("Mammal", "Mammal"),
        ("Bird", "Bird"),
        ("Reptile", "Reptile"),
        ("Fish", "Fish"),
        ("Amphibian", "Amphibian"),
    ]

    DIET_CHOICES = [
        ("Carnivore", "Carnivore"),
        ("Herbivore", "Herbivore"),
        ("Omnivore", "Omnivore"),
    ]

    HEALTH_STATUS_CHOICES = [
        ("Healthy", "Healthy"),
        ("Under Observation", "Under Observation"),
        ("Under Treatment", "Under Treatment"),
        ("Recovering", "Recovering"),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150, blank=True, null=True)
    age = models.IntegerField()
    habitat = models.CharField(max_length=100)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True
    )

    diet = models.CharField(
        max_length=20,
        choices=DIET_CHOICES,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    health_status = models.CharField(
        max_length=30,
        choices=HEALTH_STATUS_CHOICES,
        default="Healthy"
    )

    image = models.ImageField(
        upload_to="animals/",
        blank=True,
        null=True
    )

    assigned_staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="animals"
    )

    def __str__(self):
        return self.name