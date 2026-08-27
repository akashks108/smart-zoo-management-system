from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.feedback_page,
        name="feedback"
    ),

    path(
        "admin/",
        views.admin_feedback,
        name="admin_feedback"
    ),

    path(
    "admin/delete/<int:feedback_id>/",
    views.delete_feedback,
    name="delete_feedback"
    ),

]