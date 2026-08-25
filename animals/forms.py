from django import forms
from .models import Animal


class AnimalForm(forms.ModelForm):

    class Meta:

        model = Animal

        fields = [
            "name",
            "species",
            "scientific_name",
            "age",
            "habitat",
            "category",
            "diet",
            "description",
            "image",
            "assigned_staff",
        ]

        widgets = {

            "name": forms.TextInput(attrs={"class": "form-control"}),

            "species": forms.TextInput(attrs={"class": "form-control"}),

            "scientific_name": forms.TextInput(attrs={"class": "form-control"}),

            "age": forms.NumberInput(attrs={"class": "form-control"}),

            "habitat": forms.TextInput(attrs={"class": "form-control"}),

            "category": forms.Select(attrs={"class": "form-control"}),

            "diet": forms.Select(attrs={"class": "form-control"}),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),

            "image": forms.FileInput(attrs={
                "class": "form-control",
                "id": "image-input"
            }),

            "assigned_staff": forms.Select(attrs={
            "class": "form-control"
            }),

        }