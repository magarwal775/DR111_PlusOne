from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Alumni, Faculty, User

admin.site.register(Alumni)
admin.site.register(Faculty)
admin.site.register(User)
