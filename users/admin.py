from django.contrib import admin

from users.models import User

from lms.models import Subscription, Course


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        "id",
        "email",
    )


admin.site.register(Subscription)
admin.site.register(Course)