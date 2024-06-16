from django.contrib import admin

from authentication.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass