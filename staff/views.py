from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Staff
from django.shortcuts import render, redirect
from .forms import StaffForm, StaffEditForm

@login_required
def staff_list(request):

    search = request.GET.get("search", "")

    if search:
        staff = Staff.objects.filter(
        Q(user__first_name__icontains=search) |
        Q(user__last_name__icontains=search) |
        Q(user__username__icontains=search) |
        Q(designation__icontains=search) |
        Q(department__icontains=search)
    )
    else:
        staff = Staff.objects.all()

    context = {
        "staff": staff,
        "search": search or "",
    }

    return render(request, "staff/staff_list.html", context)

@login_required
def add_staff(request):

    if request.method == "POST":

        form = StaffForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, "staff/add_staff.html", {"form": form})

            user = User.objects.create_user(

                username=username,

                password=form.cleaned_data["password"],

                first_name=form.cleaned_data["first_name"],

                last_name=form.cleaned_data["last_name"]

            )

            Staff.objects.create(

                user=user,

                designation=form.cleaned_data["designation"],

                department=form.cleaned_data["department"]

            )
            messages.success(
                request,
                f"{user.first_name} {user.last_name} added successfully."
            )

            return redirect("staff_list")

    else:

        form = StaffForm()

    return render(
    request,
    "staff/add_staff.html",
    {
        "form": form,
        "title": "Add New Staff",
        "button_text": "Save Staff",
    }
 )

@login_required

def edit_staff(request, id):

    staff = Staff.objects.get(id=id)
    user = staff.user

    if request.method == "POST":

        form = StaffEditForm(request.POST)

        if form.is_valid():

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            staff.designation = form.cleaned_data["designation"]
            staff.department = form.cleaned_data["department"]
            staff.save()

            messages.success(request, f"{staff.user.first_name} updated successfully.")

            return redirect("staff_list")

    else:

        form = StaffEditForm(
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "designation": staff.designation,
                "department": staff.department,
            }
        )

    return render(
        request,
        "staff/add_staff.html",
        {
            "form": form,
            "title": "Edit Staff",
            "button_text": "Update Staff",
        }
    )


@login_required
def delete_staff(request, id):

    staff = Staff.objects.get(id=id)

    if request.method == "POST":

        user = staff.user

        staff.delete()
        user.delete()

        messages.success(
            request,
            f"Staff '{staff.user.username}' deleted successfully."
)

        return redirect("staff_list")

    return render(
        request,
        "staff/delete_staff.html",
        {
            "staff": staff
        }
    )

def staff_login(request):

    if request.user.is_authenticated:
        return redirect("staff_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Check whether this user is a staff member
            if Staff.objects.filter(user=user).exists():

                login(request, user)

                messages.success(
                    request,
                    f"Welcome, {user.first_name}!"
                )

                return redirect("staff_dashboard")

            else:

                messages.error(
                    request,
                    "You are not authorized as staff."
                )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "staff/login.html")

def staff_logout(request):

    logout(request)

    return redirect("login")