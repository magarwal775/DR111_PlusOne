from django.db import models
from college.models import College

# Create your models here.
class DonationType(models.Model):
    donation_id = models.CharField(
        max_length=100,
        null=False,
        help_text="Donation ID for the type of donation same as the stripe dashboard",
    )
    donation_name = models.CharField(
        max_length=100, null=True, help_text="Formal Name of the donation"
    )
    description = models.TextField(help_text="What the donation is for", default="ABC")
    image = models.ImageField(blank=True, null=True, upload_to="donation_images/")
    date_time = models.DateTimeField(auto_now=True)
    days_remaining = models.IntegerField(blank=True, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.donation_id


class DonationAmount(models.Model):
    donation = models.ForeignKey(DonationType, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False, help_text="The chosen amount of Donation")

    def __str__(self):
        return self.donation.donation_id + " : " + str(self.amount)
