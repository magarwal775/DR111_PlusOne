from django.shortcuts import render
from mailer.forms import MailComposeForm
from mailer.models import MailSent
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from college.models import College
from html2text import html2text
from django.contrib.auth import get_user_model

user_login_required = user_passes_test(lambda user: user.is_superuser, login_url="/")
def active_user(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func

def check_mail_config():
    if hasattr(settings, "EMAIL_HOST_USER") and hasattr(
        settings, "EMAIL_HOST_PASSWORD"
    ):
        if (
            settings.EMAIL_HOST_USER != "None"
            and settings.EMAIL_HOST_PASSWORD != "None"
        ):
            return True
    return False


@active_user
def index(req):
    conf_check = check_mail_config()
    history = MailSent.objects.all()
    return render(req, "mailer/index.html", {"history": history, "check": conf_check})


@active_user
def compose_mail(req):
    form = MailComposeForm()
    return render(req, "mailer/compose.html", {"form": form})


@active_user
def send_mail(req):
    if req.method == "POST":
        subject = req.POST["subject"]
        body = req.POST["body"]
        file = ""
        try:
            to = req.POST["to"]
        except:
            pass
        college = req.POST["college"]
        try:
            file = req.FILES["attachment"]
        except:
            pass
        if college != "":
            temp = []
            User = get_user_model()
            for user in User.objects.filter(college = College.objects.get(name = college)):
                temp.append(user.email)
            to = temp
        else:
            to = to.split(",")
        html_msg = body
        text_msg = html2text(body)
        from_email = settings.EMAIL_HOST_USER

        msg = EmailMultiAlternatives(subject, text_msg, from_email, to)
        msg.attach_alternative(html_msg, "text/html")
        if file != "":
            msg.attach(file.name, file.read(), file.content_type)
        try:
            msg.send()
            m = MailSent(
                subject=subject,
                body=text_msg,
                from_email=from_email,
                to=str(to),
                sent_by=req.user,
                time=timezone.now(),
            )
            m.save()

            messages.add_message(req, messages.SUCCESS, "Email successfully sent")
        except Exception as e:
            print("ERROR in SMTP :: ", e)
            messages.add_message(
                req, messages.ERROR, "An error occured. Check configuration again."
            )
        return HttpResponseRedirect("/mail/")
    else:
        form = MailComposeForm()
        return HttpResponseRedirect("/mail/compose/", {"form": form})
