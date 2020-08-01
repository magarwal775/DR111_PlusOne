from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from college.models import College, Course, Department, Specialization

admin.site.register(College)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Specialization)
