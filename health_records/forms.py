from django import forms
from .models import HealthRecord


class HealthRecordForm(forms.ModelForm):

    class Meta:
        model = HealthRecord

        fields = [
            "diagnosis",
            "treatment",
            "checkup_date",
            "veterinarian",
            "remarks",
        ]

        widgets = {

            "checkup_date": forms.DateInput(
                attrs={"type": "date"}
            ),

            "diagnosis": forms.TextInput(
                attrs={
                    "placeholder": "Enter diagnosis"
                }
            ),

            "treatment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter treatment"
                }
            ),

            "veterinarian": forms.TextInput(
                attrs={
                    "placeholder": "Veterinarian name"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Additional remarks"
                }
            ),
        }