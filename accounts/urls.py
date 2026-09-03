from django.urls import path
from . import views


urlpatterns = [

    path(
        "login/",
        views.admin_login,
        name="login"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),
    path(
    "profile/",
    views.profile,
    name="profile"
    ),

    path("profile/edit/", views.edit_profile, name="visitor_edit_profile"),  

]