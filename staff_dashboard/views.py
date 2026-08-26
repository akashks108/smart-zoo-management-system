from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from staff.forms import StaffProfileForm

from animals.models import Animal


@login_required
def staff_dashboard(request):

    assigned_animals = Animal.objects.filter(
        assigned_staff=request.user.staff
    )

    context = {
        "staff": request.user.staff,
        "assigned_animals": assigned_animals,
        "total_animals": assigned_animals.count(),
    }

    return render(
        request,
        "staff_dashboard/dashboard.html",
        context
    )


@login_required
def my_animals(request):

    assigned_animals = Animal.objects.filter(
        assigned_staff=request.user.staff
    )

    return render(
        request,
        "staff_dashboard/my_animals.html",
        {
            "assigned_animals": assigned_animals
        }
    )

@login_required
def my_profile(request):

    staff = request.user.staff

    context = {
        "staff": staff,
    }

    return render(
        request,
        "staff_dashboard/my_profile.html",
        context
    )

@login_required
def edit_profile(request):

    staff = request.user.staff
    user = request.user

    if request.method == "POST":

        form = StaffProfileForm(request.POST)

        if form.is_valid():

            current_password = form.cleaned_data["current_password"]
            new_password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]

            # Update personal information
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]

            # Change password only if the user entered password fields
            if current_password or new_password or confirm_password:

                if not current_password:
                    form.add_error(
                        "current_password",
                        "Enter your current password."
                    )

                elif not user.check_password(current_password):
                    form.add_error(
                        "current_password",
                        "Current password is incorrect."
                    )

                elif not new_password:
                    form.add_error(
                        "new_password",
                        "Enter a new password."
                    )

                elif new_password != confirm_password:
                    form.add_error(
                        "confirm_password",
                        "New passwords do not match."
                    )

                else:
                    user.set_password(new_password)

            if not form.errors:

                user.save()

                messages.success(
                    request,
                    "Profile updated successfully."
                )

                return redirect("my_profile")

    else:

        form = StaffProfileForm(
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        )

    context = {
        "staff": staff,
        "form": form,
    }

    return render(
        request,
        "staff_dashboard/edit_profile.html",
        context
    )
