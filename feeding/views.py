from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from animals.models import Animal
from .models import FeedingSchedule
from .forms import FeedingScheduleForm


def feeding_schedule_list(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id
    )

    feeding_records = FeedingSchedule.objects.filter(
        animal=animal
    ).order_by("-feeding_date", "-feeding_time")

    context = {
        "animal": animal,
        "feeding_records": feeding_records,
    }

    return render(
        request,
        "feeding/feeding_schedule_list.html",
        context
    )


def add_feeding_schedule(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id
    )

    if request.method == "POST":

        form = FeedingScheduleForm(request.POST)

        if form.is_valid():

            record = form.save(commit=False)

            record.animal = animal

            record.save()
            messages.success(
                request,
                "Feeding schedule added successfully."
            )

            return redirect(
                "feeding_schedule_list",
                animal_id=animal.id
            )

    else:

        form = FeedingScheduleForm()

    context = {
        "animal": animal,
        "form": form,
    }

    return render(
        request,
        "feeding/add_feeding_schedule.html",
        context
    )

def edit_feeding_schedule(request, id):

    record = get_object_or_404(
        FeedingSchedule,
        id=id
    )

    animal = record.animal

    if request.method == "POST":

        form = FeedingScheduleForm(
            request.POST,
            instance=record
        )

        if form.is_valid():

            form.save()
            messages.success(
                request,
                "Feeding schedule updated successfully."
            )

            return redirect(
                "feeding_schedule_list",
                animal_id=animal.id
            )

    else:

        form = FeedingScheduleForm(
            instance=record
        )

    context = {
        "animal": animal,
        "record": record,
        "form": form,
    }

    return render(
        request,
        "feeding/edit_feeding_schedule.html",
        context
    )
def delete_feeding_schedule(request, id):

    record = get_object_or_404(
        FeedingSchedule,
        id=id
    )

    animal = record.animal

    if request.method == "POST":

        record.delete()

        messages.success(
            request,
            "Feeding schedule deleted successfully."
        )

        return redirect(
            "feeding_schedule_list",
            animal_id=animal.id
        )

    context = {
        "animal": animal,
        "record": record,
    }

    return render(
        request,
        "feeding/delete_feeding_schedule.html",
        context
    )