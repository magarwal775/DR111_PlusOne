from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Alumni, Faculty, User, JobHistory, Organisation

admin.site.register(Alumni)
admin.site.register(Faculty)
admin.site.register(User)
admin.site.register(JobHistory)
admin.site.register(Organisation)
