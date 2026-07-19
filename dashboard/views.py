from django.shortcuts import render
from animals.models import Animal

def dashboard(request):

    total_animals = Animal.objects.count()

    context = {
        "total_animals": total_animals,
    }

    return render(request, "dashboard/dashboard.html", context)