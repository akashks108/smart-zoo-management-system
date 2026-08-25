from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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

    return render(request, "staff_dashboard/dashboard.html", context)

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