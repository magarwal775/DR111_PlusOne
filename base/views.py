from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.models import Alumni, Faculty, User
from base.models import Event, Notice, News, Story, Gallery, Carousel
from jobs.models import Job
from payments.models import DonationType
from django.db.models import Q
import datetime
from django.http import JsonResponse
from .filters import UserFilter
from base.forms import AddEvent, AddNews, AddStory
from college.models import College, Department
from accounts.decorators import alumni_required, faculty_required, verify_required

def base(request):
    return render(request, "base.html")


def home(request):
    user = request.user
    context = {}

    if user.is_authenticated:
        if user.is_alumni:
            alumni = Alumni.objects.get(user=user)
            if not user.profile_complete:
                return redirect("accounts:complete_alumni_profile")
            context["is_alumni"] = 1
            context["is_faculty"] = 0
            context["alumni"] = alumni
        elif user.is_faculty:
            faculty = Faculty.objects.get(user=user)
            if not user.profile_complete:
                return redirect("accounts:complete_faculty_profile")
            context["is_alumni"] = 0
            context["is_faculty"] = 1
            context["faculty"] = faculty
        else:
            context["is_superuser"] = 1

    if not user.is_authenticated or (user.is_authenticated and not user.college):
        events = Event.objects.all().order_by("-start_date")
        if events.count() < 3:
            context["eventsitem"] = events
        else:
            context["eventsitem"] = events[0:3]
        context["lastevent"] = events.last()

        news = News.objects.all().order_by("-date_time")
        if news.count() < 3:
            context["newsitem"] = news
        else:
            context["newsitem"] = news[0:3]
        context["lastnews"] = news.last()

        jobs = Job.objects.all().order_by("-date_created")
        if jobs.count() < 2:
            context["jobsitem"] = jobs
        else:
            context["jobsitem"] = jobs[0:2]
        context["lastjob"] = jobs.first()

        story = Story.objects.all().order_by("-date_time")
        if story.count() > 0:
            context["storyitem"] = story[0]

        donation = DonationType.objects.all().order_by("-date_time")
        if donation.count() > 1:
            context["donation"] = donation[0:2]
        else:
            context["donation"] = donation

        galleryimgs = Gallery.objects.all().order_by("-date_time")
        context['gallery'] = galleryimgs[0:6]
        carousel_images = Carousel.objects.all().order_by('-date_time')
        context['carouselimages'] = carousel_images[0:6]

    elif user.is_authenticated and (user.is_alumni or user.is_faculty):
        events = Event.objects.filter(college = user.college).order_by("-start_date")
        context["eventsitem"] = events[0:3]
        context["lastevent"] = events.last()

        news = News.objects.filter(college = user.college).order_by("-date_time")
        context["newsitem"] = news[0:3]
        context["lastnews"] = news.last()

        jobs = Job.objects.filter(college = user.college or not college).order_by("-date_created")
        context["jobsitem"] = jobs[0:2]
        context["lastjob"] = jobs.first()

        story = Story.objects.filter(college = user.college).order_by("-date_time")
        if story.count() > 0:
            context["storyitem"] = story[0]

        donation = DonationType.objects.filter(college = user.college or not college).order_by("-date_time")
        context["donation"] = donation[0:2]

        galleryimgs = Gallery.objects.filter(college = user.college or not college).order_by("-date_time")
        context['gallery'] = galleryimgs[0:6]

        carousel_images = Carousel.objects.filter(college = user.college or not college).order_by('-date_time')
        context['carouselimages'] = carousel_images[0:6]

    return render(request, "home.html", context)


def allnews(request):
    context = {}
    user = request.user
    if(not user.is_authenticated or (user.is_authenticated and not user.college)):
        news = News.objects.order_by('-date_time')
        context["news"] = news
    else:
        news = News.objects.filter(college = user.college).order_by('-date_time')
        context["news"] = news

    return render(request, "all-news.html", context)


def allevents(request):
    context = {}
    user = request.user

    if(not user.is_authenticated or (user.is_authenticated and not user.college)):
        today = datetime.datetime.today()
        upcoming_events = Event.objects.filter(Q(start_date__gte=today))
        past_events = Event.objects.filter(Q(start_date__lt=today))
        context["upcoming_events"] = upcoming_events
        context["past_events"] = past_events
    else:
        today = datetime.datetime.today()
        upcoming_events = Event.objects.filter(Q(start_date__gte=today)).filter(college = user.college)
        past_events = Event.objects.filter(Q(start_date__lt=today)).filter(college = user.college)
        context["upcoming_events"] = upcoming_events
        context["past_events"] = past_events

    return render(request, "all-events.html", context)

def allstory(request):
    context = {}
    user = request.user

    if(not user.is_authenticated or (user.is_authenticated and not user.college)):
        stories = Story.objects.order_by('-date_time')
        context["stories"] = stories
    else:
        stories = Story.objects.filter(college=user.college).order_by('-date_time')
        context["stories"] = stories

    return render(request,"all-stories.html",context)

def speceficevent(request, event_id):
    context = {}
    event = Event.objects.get(id=event_id)
    context["event"] = event

    return render(request, "specific-event.html", context)


def speceficnews(request, news_id):
    context = {}
    news = News.objects.get(id=news_id)
    context["news"] = news

    return render(request, "specefic-news.html", context)


def speceficstory(request, story_id):
    context = {}
    story = Story.objects.get(id=story_id)
    context["story"] = story

    return render(request, "specefic-story.html", context)


def profile(request, user_name, user_id):
    context = {}
    if request.POST:
        alumni = Alumni.objects.get(user_id=user_id)
        alumni.profile_verified = 1
        alumni.save()
        return redirect('base:verification_alumni')

    user = User.objects.get(id=user_id)
    if user.is_alumni:
        alumni = Alumni.objects.get(user=user)
        context["is_alumni"] = 1
        context["is_faculty"] = 0
        context["alumni"] = alumni
    elif user.is_faculty:
        faculty = Faculty.objects.get(user=user)
        context["is_alumni"] = 0
        context["is_faculty"] = 1
        context["faculty"] = faculty
    context["user"] = user
    context["editprofile"] = 0
    if user == request.user:
        context["editprofile"] = 1

    return render(request, "profile.html", context)


def searchalumni(request):
    context = {}
    user_list = User.objects.filter(is_alumni=1)
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'search_alumni.html', {'filter': user_filter})

def get_queryset(query=None):
    queryset = {}
    if query:
        alumnis = (
            User.objects.filter(Q(full_name__icontains=query))
            .filter(is_alumni=1)
            .distinct()
        )
        queryset["users"] = alumnis
    return queryset


def autocomplete(request):
    if "term" in request.GET:
        qs = (
            User.objects.filter(Q(full_name__icontains=request.GET["term"]))
            .filter(is_alumni=True)
            .distinct()
        )
        names = list()
        for name in qs:
            names.append(name.full_name)
        return JsonResponse(names, safe=False)
    return JsonResponse({}, safe=False)

def jobsection(request):
    context = {}
    jobs=Job.objects.all()
    context['jobsitem']=jobs
    return render(request,'all-jobs.html',context)

def verification_alumni(request):
    context = {}
    account = Alumni.objects.filter(profile_verified=0)
    if account.count()<1:
        context["number"] = 1
    context["account"] = account
    return render(request, 'verification-request-list.html', context)

def addevent(request):

    context = {}

    user = request.user

    if request.POST:
        form = AddEvent(request.POST)
        if form.is_valid():
            current = form.save(commit=False)
            current.user=request.user
            current.save()
            return redirect("base:allevents")
    else:
        form = AddEvent()

    context["form"] = form
    return render(request, "addevent.html", context)

def addnews(request):

    context = {}

    user = request.user

    if request.POST:
        form = AddNews(request.POST)
        if form.is_valid():
            current = form.save(commit=False)
            current.user=request.user
            current.save()
            return redirect("base:allnews")
    else:
        form = AddNews()

    context["form"] = form
    return render(request, "addnews.html", context)

def addstory(request):

    context = {}

    user = request.user

    if request.POST:
        form = AddStory(request.POST)
        if form.is_valid():
            current = form.save(commit=False)
            current.user=request.user
            current.save()
            return redirect("base:home")
    else:
        form = AddStory()

    context["form"] = form
    return render(request, "addstory.html", context)
