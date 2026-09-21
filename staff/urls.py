from django.urls import path
from . import views

urlpatterns = [
    path("", views.staff_list, name="staff_list"),
    path("add/", views.add_staff, name="add_staff"),
    path("edit/<int:id>/", views.edit_staff, name="edit_staff"),
    path("delete/<int:id>/", views.delete_staff, name="delete_staff"),
    path("logout/",views.staff_logout,name="staff_logout"),
    path("apply-leave/",views.apply_leave,name="apply_leave"),
]