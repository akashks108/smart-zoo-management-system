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

            if user.is_superuser:

                login(request, user)

                return redirect("/dashboard/")

            else:

                messages.error(
                    request,
                    "You are not authorized to access the Admin Panel."
                )

        else:

            messages.error(request, "Invalid Username or Password")

    return render(request, "accounts/login.html")