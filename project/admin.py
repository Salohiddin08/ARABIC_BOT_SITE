from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "phone_number", "verification_code", "is_verified")
    fields = ("username", "phone_number", "verification_code", "code_expiration", "is_verified")

    def save_model(self, request, obj, form, change):
        if not obj.verification_code or not obj.code_expiration:
            obj.set_verification_code()
        super().save_model(request, obj, form, change)
    