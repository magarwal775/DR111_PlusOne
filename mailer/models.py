from django.db import models
from django.conf import settings

# Create your models here.
class MailSent(models.Model):
    subject = models.CharField(max_length=1024)
    body = models.TextField(blank=True, null=True)
    from_email = models.CharField(max_length=512)
    to = models.CharField(max_length=1024)
    attachment = models.BooleanField(default=False)

    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.subject
