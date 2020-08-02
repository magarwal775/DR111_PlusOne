from django.urls import path

from base.views import(
    base,
    home,
    allnews,
    allevents,
    allstory,
    speceficevent,
    speceficnews,
    profile,
    searchalumni,
    speceficstory,
    autocomplete,
    jobsection,
    verification_alumni,
    addnews,
    addstory,
    addevent,
    send_p2pnotifs,
    notifications,
    notif_read
)

app_name='base'

urlpatterns = [
    path('', home, name="home"),
    path('profile/<slug:user_name>/<int:user_id>', profile, name="profile"),
    path('event/<int:event_id>', speceficevent, name="speceficevent"),
    path('news/<int:news_id>', speceficnews, name="speceficnews"),
    path('story/<int:story_id>', speceficstory, name="speceficstory"),
    path('news', allnews, name="allnews"),
    path('events', allevents, name="allevents"),
    path('stories',allstory,name="allstory"),
    path('searchalumni', searchalumni, name="searchalumni"),
    path('autocomplete', autocomplete, name="autocomplete"),
    path('jobsection', jobsection,name="jobsection"),
    path('verifialumni', verification_alumni, name="verification_alumni"),
    path('addstory', addstory, name="addstory"),
    path('addevent', addevent, name="addevent"),
    path('addnews', addnews, name="addnews"),
    path('sendnotifs/', send_p2pnotifs, name="sendnotifs"),
    path('notifications/', notifications, name="notifications"),
    path('notifsread/',notif_read, name="readnotifs")
]
