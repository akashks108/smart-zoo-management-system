from django import forms


class StaffForm(forms.Form):

    first_name = forms.CharField(max_length=100)

    last_name = forms.CharField(max_length=100)

    username = forms.CharField(max_length=50)

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    designation = forms.ChoiceField(
        choices=[
            ("Zoo Keeper", "Zoo Keeper"),
            ("Veterinarian", "Veterinarian"),
            ("Receptionist", "Receptionist"),
            ("Security", "Security"),
            ("Cleaner", "Cleaner"),
            ("Manager", "Manager"),
        ]
    )

    department = forms.ChoiceField(
        choices=[
            ("Animal Care", "Animal Care"),
            ("Medical", "Medical"),
            ("Administration", "Administration"),
            ("Security", "Security"),
            ("Maintenance", "Maintenance"),
        ]
    )

    def __init__(self, *args, **kwargs):
        readonly_username = kwargs.pop("readonly_username", False)
        super().__init__(*args, **kwargs)

        if readonly_username:
            self.fields["username"].widget.attrs["readonly"] = True
            self.fields["password"].required = False

class StaffEditForm(forms.Form):

    first_name = forms.CharField(max_length=100)

    last_name = forms.CharField(max_length=100)

    designation = forms.ChoiceField(
        choices=[
            ("Zoo Keeper", "Zoo Keeper"),
            ("Veterinarian", "Veterinarian"),
            ("Receptionist", "Receptionist"),
            ("Security", "Security"),
            ("Cleaner", "Cleaner"),
            ("Manager", "Manager"),
        ]
    )

    department = forms.ChoiceField(
        choices=[
            ("Animal Care", "Animal Care"),
            ("Medical", "Medical"),
            ("Administration", "Administration"),
            ("Security", "Security"),
            ("Maintenance", "Maintenance"),
        ]
    )
class StaffProfileForm(forms.Form):

    first_name = forms.CharField(
        max_length=100
    )

    last_name = forms.CharField(
        max_length=100
    )

    email = forms.EmailField(
        required=False
    )

    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter current password"
            }
        )
    )

    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter new password"
            }
        )
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm new password"
            }
        )
    )