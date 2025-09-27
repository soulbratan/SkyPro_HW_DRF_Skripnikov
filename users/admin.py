from django.contrib import admin

from lms.models import Course, Subscription
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        "id",
        "email",
    )


admin.site.register(Subscription)
admin.site.register(Course)
