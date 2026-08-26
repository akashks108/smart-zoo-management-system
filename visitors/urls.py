from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.visitor_home,
        name="visitor_home"
    ),

    path(
        "animals/",
        views.animal_gallery,
        name="animal_gallery"
    ),

    path(
        "animal/<int:animal_id>/",
        views.animal_detail,
        name="animal_detail"
    ),

]