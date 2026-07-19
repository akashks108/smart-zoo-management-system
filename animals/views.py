from urllib import request

from django.contrib import messages
from django.shortcuts import render,redirect
from django.db.models import Q
from .models import Animal
from .forms import AnimalForm


def home(request):
    animals = Animal.objects.all()
    return render(
        request,
        "animals/home.html",
        {
            "animals": animals
        }
    )

def animal_list(request):

    search = request.GET.get("search", "")

    if search:
        animals = Animal.objects.filter(
            Q(name__icontains=search) |
            Q(species__icontains=search) |
            Q(category__icontains=search) |
            Q(diet__icontains=search)
        )
    else:
        animals = Animal.objects.all()

    return render(
        request,
        "animals/animal_list.html",
        {
            "animals": animals,
            "search": search,
        }
    )

def add_animal(request):

    if request.method == "POST":

        form = AnimalForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            messages.success(request, f"{form.cleaned_data['name']} added successfully.")

            return redirect("animal_list")  

    else:

        form = AnimalForm()

    context = {
    "form": form,
    "title": "Add New Animal",
    "button_text": "Save Animal",
}

    return render(request, "animals/animal_form.html", context)


def edit_animal(request, id):

    animal = Animal.objects.get(id=id)

    if request.method == "POST":

        form = AnimalForm(
            request.POST,
            request.FILES,
            instance=animal
        )

        if form.is_valid():

            form.save()
            messages.success(request, f"{animal.name} updated successfully.")
            return redirect("animal_list")

    else:

        form = AnimalForm(instance=animal)

    return render(
    request,
    "animals/animal_form.html",
    {
        "form": form,
        "title": "Edit Animal",
        "button_text": "Update Animal",
    }
)

def delete_animal(request, id):

    animal = Animal.objects.get(id=id)

    if request.method == "POST":

        animal_name = animal.name

        animal.delete()

        messages.success(
            request,
            f"{animal.name} deleted successfully."
        )

        return redirect("animal_list")

    return render(
        request,
        "animals/delete_animal.html",
        {
            "animal": animal
        }
    )

