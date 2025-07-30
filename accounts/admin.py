from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created")


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "email",
        "full_name",
        "is_admin",
    )
    list_filter = ("is_admin",)

    fieldsets = (
        (None, {"fields": ("email", "phone_number", "full_name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_admin","is_superuser", "last_login", 'groups', 'user_permissions')}),
    )

    # 👇👇 این بخش رو اضافه کن تا مشکل username و usable_password حل بشه
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "email",
                    "full_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("email", "full_name")
    ordering = ("full_name",)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
