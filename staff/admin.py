from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = (
        "get_full_name",
        "get_username",
        "designation",
        "department",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "designation",
        "department",
    )

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    get_full_name.short_description = "Name"

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "Username"