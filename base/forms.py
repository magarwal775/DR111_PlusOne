from django import forms
from base.models import Event, News, Story, EventRegistrationList


class AddEvent(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'start_date', 'end_date', 'start_time', 'end_time', 'venue', 'image', 'body')


class AddNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'body', 'image')


class AddStory(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'body')


class EventRegistration(forms.ModelForm):
    class Meta:
        model = EventRegistrationList
        fields = ('name', 'email')
