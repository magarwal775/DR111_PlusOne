from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Alumni, Faculty, User, JobHistory, Organisation

class UserCustomAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Alumni)
admin.site.register(Faculty)
admin.site.register(User, UserCustomAdmin)
admin.site.register(JobHistory)
admin.site.register(Organisation)
