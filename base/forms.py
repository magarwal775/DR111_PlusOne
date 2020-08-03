from django import forms
from base.models import Event, News, Story, EventRegistrationList,Recommendation
from accounts.models import JobHistory, Organisation
import datetime

def year_choices():
    return [(r, r) for r in range(1947, datetime.date.today().year + 1)]

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


class Recommend(forms.ModelForm):

    Year_Passing = forms.ChoiceField(choices=year_choices())
    class Meta:
        model = Recommendation
        fields = ('first_name','last_name','email','college','Year_Passing','facebook_profile','linkedin_profile')

class UpdateJobHistory(forms.ModelForm):
    class Meta:
        model = JobHistory
        fields = ('organisation', 'title', 'year_started', 'year_left')

class AddJobHistory(forms.ModelForm):
    class Meta:
        model = JobHistory
        fields = ('organisation', 'title', 'year_started', 'year_left')
