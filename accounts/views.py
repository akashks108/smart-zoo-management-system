from staff.models import Staff
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def admin_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:

                return redirect("dashboard")

            elif Staff.objects.filter(user=user).exists():

                return redirect("staff_dashboard")

            else:

                messages.error(
                    request,
                    "You are not authorized to access this system."
                )

                return redirect("login")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "accounts/login.html")