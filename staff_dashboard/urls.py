from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.staff_dashboard,
        name="staff_dashboard"
    ),

    path(
        "my-animals/",
        views.my_animals,
        name="my_animals"
    ),

    path(
    "profile/",
    views.my_profile,
    name="my_profile"
    ),

    path(
    "profile/edit/",
    views.edit_profile,
    name="edit_profile"
    ),
 

]