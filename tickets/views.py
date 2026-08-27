from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.db.models import Sum, Count


@login_required(login_url="/accounts/login/")
def book_ticket(request):

    if request.method == "POST":

        visit_date = request.POST.get("visit_date")
        adults = int(request.POST.get("adults", 0))
        children = int(request.POST.get("children", 0))

        adult_price = 200
        child_price = 100

        total_amount = (
            adults * adult_price
            + children * child_price
        )

        # Store booking information temporarily
        request.session["visit_date"] = visit_date
        request.session["adults"] = adults
        request.session["children"] = children
        request.session["total_amount"] = total_amount

        return redirect("payment")

    return render(
        request,
        "tickets/book_ticket.html"
    )


@login_required(login_url="/accounts/login/")
def payment(request):

    total_amount = request.session.get("total_amount")

    if total_amount is None:
        return redirect("book_ticket")

    if request.method == "POST":

        visit_date = request.session.get("visit_date")
        adults = request.session.get("adults")
        children = request.session.get("children")

        # Create the booking after fake payment
        booking = Booking.objects.create(
            user=request.user,
            visit_date=visit_date,
            adults=adults,
            children=children,
            total_amount=total_amount
        )

        # Clear temporary booking information
        request.session.pop("visit_date", None)
        request.session.pop("adults", None)
        request.session.pop("children", None)
        request.session.pop("total_amount", None)

        return redirect(
            "payment_success",
            booking_id=booking.id
        )

    return render(
        request,
        "tickets/payment.html",
        {
            "total_amount": total_amount
        }
    )


@login_required(login_url="/accounts/login/")
def payment_success(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    return render(
        request,
        "tickets/payment_success.html",
        {
            "booking": booking
        }
    )

@login_required(login_url="/accounts/login/")
def download_ticket(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="zoo_ticket_{booking.id}.pdf"'
    )

    pdf = canvas.Canvas(
        response,
        pagesize=A4
    )

    width, height = A4

    # =========================
    # Colors
    # =========================

    dark_green = "#176B24"
    light_green = "#E7F3E8"
    very_light_green = "#F5F8F4"
    gray = "#666666"
    white = "#FFFFFF"

    # =========================
    # Background
    # =========================

    pdf.setFillColor(light_green)
    pdf.rect(
        0,
        0,
        width,
        height,
        fill=1,
        stroke=0
    )

    # =========================
    # Main Ticket
    # =========================

    pdf.setFillColor(white)

    pdf.roundRect(
        45,
        90,
        width - 90,
        height - 180,
        20,
        fill=1,
        stroke=0
    )

    # =========================
    # Header
    # =========================

    pdf.setFillColor(dark_green)

    pdf.roundRect(
        45,
        height - 180,
        width - 90,
        120,
        20,
        fill=1,
        stroke=0
    )

    # Cover bottom corners of header
    pdf.rect(
        45,
        height - 180,
        width - 90,
        25,
        fill=1,
        stroke=0
    )

    # Zoo title

    pdf.setFillColor(white)

    pdf.setFont(
        "Helvetica-Bold",
        30
    )

    pdf.drawCentredString(
        width / 2,
        height - 105,
        "ZOO"
    )

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 130,
        "YOUR VISIT TICKET"
    )

    # =========================
    # PAID Badge
    # =========================

    pdf.setFillColor(light_green)

    pdf.roundRect(
        width - 145,
        height - 165,
        70,
        25,
        12,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(dark_green)

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawCentredString(
        width - 110,
        height - 156,
        "PAID"
    )

    # =========================
    # Booking ID
    # =========================

    y = height - 225

    pdf.setFillColor(very_light_green)

    pdf.roundRect(
        70,
        y - 35,
        width - 140,
        55,
        10,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        90,
        y,
        "BOOKING ID"
    )

    pdf.setFillColor(dark_green)

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        90,
        y - 20,
        f"ZOO-{booking.id}"
    )

    # =========================
    # Visitor Information
    # =========================

    y -= 85

    pdf.setFillColor(dark_green)

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        75,
        y,
        "VISITOR INFORMATION"
    )

    y -= 30

    # Visitor

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        75,
        y,
        "Visitor"
    )

    pdf.setFillColor("#222222")

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        75,
        y - 18,
        booking.user.username
    )

    # Visit Date

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        310,
        y,
        "Visit Date"
    )

    pdf.setFillColor("#222222")

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    formatted_date = booking.visit_date.strftime(
        "%d %B %Y"
    )

    pdf.drawString(
        310,
        y - 18,
        formatted_date
    )

    # =========================
    # Ticket Quantities
    # =========================

    y -= 75

    pdf.setFillColor(dark_green)

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        75,
        y,
        "TICKET DETAILS"
    )

    y -= 30

    # Adult box

    pdf.setFillColor(very_light_green)

    pdf.roundRect(
        75,
        y - 45,
        200,
        55,
        10,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        90,
        y - 10,
        "ADULT TICKETS"
    )

    pdf.setFillColor(dark_green)

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        90,
        y - 32,
        str(booking.adults)
    )

    # Child box

    pdf.setFillColor(very_light_green)

    pdf.roundRect(
        300,
        y - 45,
        200,
        55,
        10,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawString(
        315,
        y - 10,
        "CHILD TICKETS"
    )

    pdf.setFillColor(dark_green)

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        315,
        y - 32,
        str(booking.children)
    )

    # =========================
    # Total Amount
    # =========================

    y -= 85

    pdf.setFillColor(dark_green)

    pdf.roundRect(
        75,
        y - 60,
        width - 150,
        65,
        12,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(white)

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        95,
        y - 30,
        "TOTAL PAID"
    )

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawRightString(
        width - 95,
        y - 31,
        f"Rs. {booking.total_amount}"
    )

    # =========================
    # Separator
    # =========================

    y -= 95

    pdf.setStrokeColor("#DDE8DE")

    pdf.line(
        75,
        y,
        width - 75,
        y
    )

    # =========================
    # Footer
    # =========================

    pdf.setFillColor(dark_green)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawCentredString(
        width / 2,
        y - 30,
        "Thank you for visiting our zoo!"
    )

    pdf.setFillColor(gray)

    pdf.setFont(
        "Helvetica",
        9
    )

    pdf.drawCentredString(
        width / 2,
        y - 48,
        "Please present this ticket at the zoo entrance."
    )

    pdf.drawCentredString(
        width / 2,
        y - 63,
        "This ticket is valid only for the selected visit date."
    )

    # =========================
    # Finish PDF
    # =========================

    pdf.showPage()

    pdf.save()

    return response

@login_required(login_url="/accounts/login/")
def my_tickets(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "tickets/my_tickets.html",
        {
            "bookings": bookings
        }
    )

@login_required
def admin_tickets(request):

    bookings = Booking.objects.select_related("user").order_by("-created_at")

    selected_month = request.GET.get("month", "")

    if selected_month:
        year, month = selected_month.split("-")

        bookings = bookings.filter(
            created_at__year=year,
            created_at__month=month
        )


    total_bookings = bookings.count()

    total_revenue = bookings.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    return render(
        request,
        "tickets/admin_tickets.html",
        {
            "bookings": bookings,
            "selected_month": selected_month,
            "total_bookings": total_bookings,
            "total_revenue": total_revenue,
        }
    )