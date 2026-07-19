from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("list/", views.animal_list, name="animal_list"),
    path("add/", views.add_animal, name="add_animal"),
    path("edit/<int:id>/", views.edit_animal, name="edit_animal"),
    path("delete/<int:id>/", views.delete_animal, name="delete_animal"),
]