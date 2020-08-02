from django.db import models
from accounts.models import User, Alumni, Faculty
from college.models import College

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    organisation = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
