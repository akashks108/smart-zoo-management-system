from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="dashboard"),

    path(
        "leave/<int:id>/<str:status>/",
        views.update_leave_status,
        name="update_leave_status"
    ),

]