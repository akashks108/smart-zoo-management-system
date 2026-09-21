import json

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from animals.models import Animal
from staff.models import Staff
from tickets.models import Booking
from staff.models import LeaveRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def dashboard(request):

    total_animals = Animal.objects.count()
    total_staff = Staff.objects.count()
    todays_visitors = Booking.objects.filter(visit_date=timezone.localdate()).aggregate(total=Sum("adults") + Sum("children"))["total"] or 0
    leave_requests = LeaveRequest.objects.filter(status="Pending").select_related("staff__user")

    period = request.GET.get("period", "all")

    today = timezone.localdate()

    bookings = Booking.objects.all()

    if period == "this_month":

        bookings = bookings.filter(
            visit_date__year=today.year,
            visit_date__month=today.month
        )

    elif period == "last_month":

        last_month = today - relativedelta(months=1)

        bookings = bookings.filter(
            visit_date__year=last_month.year,
            visit_date__month=last_month.month
        )

    elif period == "last_3_months":

        start_date = today - relativedelta(months=3)

        bookings = bookings.filter(
            visit_date__gte=start_date,
            visit_date__lte=today
        )

    elif period == "this_year":

        bookings = bookings.filter(
            visit_date__year=today.year
        )

    bookings = (
        bookings
        .values("visit_date")
        .annotate(revenue=Sum("total_amount"))
        .order_by("visit_date")
    )

    revenue_data = []

    for booking in bookings:

        revenue_data.append({
            "date": booking["visit_date"].strftime("%d %b"),
            "revenue": float(booking["revenue"] or 0),
        })

    context = {
        "total_animals": total_animals,
        "total_staff": total_staff,
        "todays_visitors": todays_visitors,
        "revenue_data": json.dumps(revenue_data),
        "period": period,
        "leave_requests": leave_requests,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )

@login_required
def update_leave_status(request, id, status):

    leave_request = get_object_or_404(
        LeaveRequest,
        id=id
    )

    if status == "Approved":
        leave_request.status = "Approved"

    elif status == "Rejected":
        leave_request.status = "Rejected"

    leave_request.save()

    messages.success(
        request,
        f"Leave request {status.lower()} successfully."
    )

    return redirect("dashboard")