from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace="base")),
    path('', include('accounts.urls')),
    path('', include('college.urls')),
    path('', include('chat.urls')),
    path('', include('payments.urls')),
    path('mail/',include('mailer.urls')),
    path('email/',include(mail_urls)),
]

urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
