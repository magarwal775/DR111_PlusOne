from django.contrib import admin
from payments.models import DonationType, DonationAmount

# Register your models here.
admin.site.register(DonationType)
admin.site.register(DonationAmount)