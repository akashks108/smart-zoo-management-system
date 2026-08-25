from django.urls import path
from . import views

urlpatterns = [

    path(
        "<int:animal_id>/",
        views.health_record_list,
        name="health_record_list"
    ),

    path(
        "<int:animal_id>/add/",
        views.add_health_record,
        name="add_health_record"
    ),

    path(
    "edit/<int:record_id>/",
    views.edit_health_record,
    name="edit_health_record"
),

path(
    "delete/<int:record_id>/",
    views.delete_health_record,
    name="delete_health_record"
),

]