from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Feedback
from django.db.models import Avg, Count
from django.shortcuts import render, redirect, get_object_or_404


@login_required(login_url="/accounts/login/")
def feedback_page(request):

    success = False

    if request.method == "POST":

        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        Feedback.objects.create(
            user=request.user,
            rating=rating,
            comment=comment
        )

        success = True

    return render(
        request,
        "feedback/feedback.html",
        {"success": success}
    )

@login_required
def admin_feedback(request):

    feedbacks = Feedback.objects.select_related("user").order_by("-created_at")

    total_feedbacks = Feedback.objects.aggregate(
        total=Count("id")
    )["total"]

    average_rating = Feedback.objects.aggregate(
        average=Avg("rating")
    )["average"] or 0

    return render(
        request,
        "feedback/admin_feedback.html",
        {
            "feedbacks": feedbacks,
            "total_feedbacks": total_feedbacks,
            "average_rating": round(average_rating, 1),
        }
    )

@login_required
def delete_feedback(request, feedback_id):

    feedback = get_object_or_404(
        Feedback,
        id=feedback_id
    )

    if request.method == "POST":
        feedback.delete()

    return redirect("admin_feedback")