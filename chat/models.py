from django.db import models
from django.conf import settings
from django.utils import timezone
from PIL import Image
import io

class Group(models.Model):
    group_id = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100, null=True, default="CHANNEL", blank=True)

    def __str__(self):
        return self.group_name + " " + self.group_id

class Messages(models.Model):
    parent_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    message_text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.localtime().now)

    def __str__(self):
        tup = tuple([self.parent_user, self.message_text])
        return str(tup)

    def last_messages(roomName, times=0):
        group = Group.objects.get_or_create(group_id=roomName)[0]
        return list(Messages.objects.filter(group=group).order_by("date_posted"))
