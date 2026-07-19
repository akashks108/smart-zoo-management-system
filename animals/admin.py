from django.contrib import admin
from .models import Animal


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "species",
        "scientific_name",
        "age",
        "habitat",
    )

    search_fields = (
        "name",
        "species",
        "scientific_name",
    )