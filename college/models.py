from django.db import models
from chat.models import Group
from hashlib import md5


class College(models.Model):
    name = models.CharField(max_length=200)
    year_of_establish = models.IntegerField()
    address = models.TextField(null=True)
    website = models.URLField(max_length=300, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        Group.objects.get_or_create(group_id = md5(self.name.encode("utf-8")).hexdigest())
        super(College, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Group.objects.get(group_id = md5(self.name.encode("utf-8")).hexdigest()).delete()
        super(College, self).delete(*args, **kwargs)

class Course(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Specialization(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
