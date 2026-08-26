from django import forms
from .models import HealthRecord
from staff.models import Staff


class HealthRecordForm(forms.ModelForm):

    class Meta:
        model = HealthRecord

        fields = [
            "diagnosis",
            "treatment",
            "checkup_date",
            "veterinarian_staff",
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

            "veterinarian_staff": forms.Select(
                attrs={}
            ),

            "remarks": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Additional remarks"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["veterinarian_staff"].queryset = Staff.objects.filter(
            designation="Veterinarian"
        )

        self.fields["veterinarian_staff"].label = "Veterinarian"
        self.fields["veterinarian_staff"].empty_label = "Select Veterinarian"