from django import forms
from .models import FeedingSchedule


class FeedingScheduleForm(forms.ModelForm):

    class Meta:
        model = FeedingSchedule

        fields = [
            "feeding_date",
            "feeding_time",
            "food",
            "quantity",
            "remarks",
        ]

        widgets = {
            "feeding_date": forms.DateInput(
                attrs={"type": "date"}
            ),

            "feeding_time": forms.TimeInput(
                attrs={"type": "time"}
            ),

            "food": forms.TextInput(
                attrs={
                    "placeholder": "Enter food"
                }
            ),

            "quantity": forms.TextInput(
                attrs={
                    "placeholder": "Enter quantity"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "placeholder": "Additional remarks",
                    "rows": 3
                }
            ),
        }