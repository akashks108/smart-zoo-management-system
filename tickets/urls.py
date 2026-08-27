from django.urls import path
from . import views


urlpatterns = [

    path(
        "book/",
        views.book_ticket,
        name="book_ticket"
    ),

    path(
        "payment/",
        views.payment,
        name="payment"
    ),

    path(
        "payment-success/<int:booking_id>/",
        views.payment_success,
        name="payment_success"
    ),

    path(
    "download-ticket/<int:booking_id>/",
    views.download_ticket,
    name="download_ticket"
    ),

    path(
    "my-tickets/",
    views.my_tickets,
    name="my_tickets"
    ),

    path(
    "admin/",
    views.admin_tickets,
    name="admin_tickets"
    ),


]