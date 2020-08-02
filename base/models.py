from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from accounts.models import User, Alumni, Faculty
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils.timezone import localdate, localtime
from college.models import College, Department


def upload_event_image_location(instance, filename):
    file_path = "event/{event_id}/{filename}".format(event_id=str(instance.id), filename=filename)
    return file_path


def upload_news_image_location(instance, filename):
    file_path = "news/{news_id}/{filename}".format(news_id=str(instance.id), filename=filename)
    return file_path


def upload_notice_image_location(instance, filename):
    file_path = "notice/{notice_id}/{filename}".format(notice_id=str(instance.id), filename=filename)
    return file_path


def upload_gallery_image_location(instance, filename):
    file_path = "gallery/{gallery_id}/{filename}".format(gallery_id=str(instance.id), filename=filename)
    return file_path


def upload_carousel_image_location(instance, filename):
    file_path = "carousel/{carousel_id}/{filename}".format(carousel_id=str(instance.id), filename=filename)
    return file_path


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    start_date = models.DateField(default=localdate)
    end_date = models.DateField(default=localdate)
    start_time = models.TimeField(default=localtime)
    end_time = models.TimeField(default=localtime)
    venue = models.CharField(max_length=300)
    image = models.ImageField(upload_to=upload_event_image_location, null=True, blank=True)
    body = models.TextField()
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, default="")

    def __str__(self):
        return self.title

    @property
    def start_date_date(self):
        return self.start_date.strftime("%d")

    @property
    def start_date_month(self):
        return self.start_date.strftime("%b")

    @property
    def start_date_year(self):
        return self.start_date.strftime("%Y")

    @property
    def start_date_day(self):
        return self.start_date.strftime("%A")


class EventRegistrationList(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.event.title


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    date_time = models.DateTimeField(auto_now=True)
    body = models.TextField()
    image = models.ImageField(upload_to=upload_event_image_location, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, default="")

    def __str__(self):
        return self.title

    @property
    def date_time_date(self):
        return self.date_time.strftime("%d")

    @property
    def date_time_month(self):
        return self.date_time.strftime("%b")

    @property
    def date_time_year(self):
        return self.date_time.strftime("%Y")

    @property
    def date_time_day(self):
        return self.date_time.strftime("%A")


class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to=upload_event_image_location, null=True, blank=True)
    body = models.CharField(max_length=1000)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, default="")
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    img = models.ImageField(upload_to=upload_gallery_image_location)
    date_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.img.name


class Carousel(models.Model):
    photo = models.ImageField(upload_to=upload_carousel_image_location)
    date_time = models.DateTimeField(auto_now=True)
    caption = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=100, null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.photo.name


class PersontoPersonNotifs(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user_id", on_delete=models.CASCADE, blank=True, null=True)
    to_user = models.ForeignKey(User, related_name="to_user_id", on_delete=models.CASCADE, blank=True, null=True)
    subject = models.TextField(max_length=150, null=True, blank=True)
    text = models.TextField(max_length=1000)
    read = models.BooleanField(default=False)

    def __str__(self):
        return "message"


@receiver(post_delete, sender=Event)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(post_delete, sender=Notice)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_Event(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_Event, sender=Event)


def pre_save_News(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title + str(instance.id))


pre_save.connect(pre_save_News, sender=News)


def pre_save_Story(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(pre_save_Story, sender=Story)
