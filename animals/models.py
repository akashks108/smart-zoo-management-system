from django.db import models

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
    image = models.ImageField(
    upload_to="animals/",
    blank=True,
    null=True
    )

    def __str__(self):
        return self.name