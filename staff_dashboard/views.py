from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from feeding.models import FeedingSchedule

from staff.forms import StaffProfileForm
from staff.models import LeaveRequest

from animals.models import Animal
from health_records.models import HealthRecord


@login_required
def staff_dashboard(request):

    assigned_animals = Animal.objects.filter(
        assigned_staff=request.user.staff
    )

    today = timezone.localdate()

    todays_feeding = FeedingSchedule.objects.filter(
        animal__in=assigned_animals,
        feeding_date=today
        ).values("animal").distinct().count()

    todays_health_checks = HealthRecord.objects.filter(
        animal__in=assigned_animals,
        checkup_date=today
        ).values("animal").distinct().count()

    context = {
        "staff": request.user.staff,
        "assigned_animals": assigned_animals,
        "total_animals": assigned_animals.count(),
        "todays_feeding": todays_feeding,
        "todays_health_checks": todays_health_checks,

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

    leave_requests = LeaveRequest.objects.filter(
        staff=staff
    ).order_by("-created_at")

    context = {
        "staff": staff,
        "leave_requests": leave_requests,
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
