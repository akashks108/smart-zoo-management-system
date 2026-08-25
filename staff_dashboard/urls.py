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

]