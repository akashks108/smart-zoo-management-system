from django.urls import path
from . import views

urlpatterns = [

    path(
        "<int:animal_id>/",
        views.feeding_schedule_list,
        name="feeding_schedule_list"
    ),

    path(
        "<int:animal_id>/add/",
        views.add_feeding_schedule,
        name="add_feeding_schedule"
    ),

    path(
    "edit/<int:id>/",
    views.edit_feeding_schedule,
    name="edit_feeding_schedule"
),

path(
    "delete/<int:id>/",
    views.delete_feeding_schedule,
    name="delete_feeding_schedule"
),

]