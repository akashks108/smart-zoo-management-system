from .forms import HealthRecordForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from animals.models import Animal
from .models import HealthRecord


def health_record_list(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id
    )

    health_records = HealthRecord.objects.filter(
        animal=animal
    ).order_by("-checkup_date")

    context = {
        "animal": animal,
        "health_records": health_records,
    }

    return render(
        request,
        "health_records/health_record_list.html",
        context
    )


def add_health_record(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id
    )

    if request.method == "POST":

        form = HealthRecordForm(request.POST)

        if form.is_valid():

            record = form.save(commit=False)

            record.animal = animal
            record.save()

            # Automatically update animal health status
            diagnosis = record.diagnosis.lower()
            treatment = record.treatment.lower()
            remarks = (record.remarks or "").lower()

            if "recover" in diagnosis or "recover" in treatment or "recover" in remarks:
                animal.health_status = "Recovering"

            elif "treatment" in diagnosis or "treatment" in treatment:
                animal.health_status = "Under Treatment"

            elif "observation" in diagnosis or "observation" in remarks:
                animal.health_status = "Under Observation"

            else:
                animal.health_status = "Healthy"

            animal.save()

            messages.success(
                request,
                "Health record added successfully."
            )

            return redirect(
                "health_record_list",
                animal_id=animal.id
            )

    else:

        form = HealthRecordForm()

    context = {
        "animal": animal,
        "form": form,
    }

    return render(
        request,
        "health_records/add_health_record.html",
        context
    )


def edit_health_record(request, record_id):

    record = get_object_or_404(
        HealthRecord,
        id=record_id
    )

    animal = record.animal

    if request.method == "POST":

        form = HealthRecordForm(
            request.POST,
            instance=record
        )

        if form.is_valid():

            record = form.save()

            # Automatically update animal health status
            diagnosis = record.diagnosis.lower()
            treatment = record.treatment.lower()
            remarks = (record.remarks or "").lower()

            if "recover" in diagnosis or "recover" in treatment or "recover" in remarks:
                animal.health_status = "Recovering"

            elif "treatment" in diagnosis or "treatment" in treatment:
                animal.health_status = "Under Treatment"

            elif "observation" in diagnosis or "observation" in remarks:
                animal.health_status = "Under Observation"

            else:
                animal.health_status = "Healthy"

            animal.save()

            messages.success(
                request,
                "Health record updated successfully."
            )

            return redirect(
                "health_record_list",
                animal_id=animal.id
            )

    else:

        form = HealthRecordForm(
            instance=record
        )

    context = {
        "animal": animal,
        "record": record,
        "form": form,
    }

    return render(
        request,
        "health_records/edit_health_record.html",
        context
    )


def delete_health_record(request, record_id):

    record = get_object_or_404(
        HealthRecord,
        id=record_id
    )

    animal = record.animal

    if request.method == "POST":

        record.delete()

        messages.success(
            request,
            "Health record deleted successfully."
        )

        return redirect(
            "health_record_list",
            animal_id=animal.id
        )

    context = {
        "record": record,
        "animal": animal,
    }

    return render(
        request,
        "health_records/delete_health_record.html",
        context
    )