from django.shortcuts import render, get_object_or_404

from animals.models import Animal


def visitor_home(request):

    total_animals = Animal.objects.count()

    context = {
        "total_animals": total_animals,
    }

    return render(
        request,
        "visitors/home.html",
        context
    )
def animal_gallery(request):

    search = request.GET.get("search", "")
    category = request.GET.get("category", "")

    animals = Animal.objects.all()

    # Search
    if search:
        animals = animals.filter(
            name__icontains=search
        ) | animals.filter(
            species__icontains=search
        ) | animals.filter(
            category__icontains=search
        )

    # Category filter
    if category:
        animals = animals.filter(
            category=category
        )

    categories = Animal.objects.values_list(
        "category",
        flat=True
    ).distinct()

    context = {
        "animals": animals,
        "search": search,
        "category": category,
        "categories": categories,
    }

    return render(
        request,
        "visitors/animal_gallery.html",
        context
    )
def animal_detail(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id
    )

    context = {
        "animal": animal,
    }

    return render(
        request,
        "visitors/animal_detail.html",
        context
    )