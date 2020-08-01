from django.db import models

# Create your models here.
class Gallery(models.Model):
    img = models.ImageField(upload_to=upload_gallery_image_location)
    date_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return self.img.name

class Carousel(models.Model):
    photo = models.ImageField(upload_to=upload_carousel_image_location)
    date_time = models.DateTimeField(auto_now=True)
    caption = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=100, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return self.photo.name