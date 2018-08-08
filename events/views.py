from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review, events, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters

import datetime

from django.contrib.auth.decorators import login_required

def review_list(request):
    latest_review_list = Review.objects.order_by('-date')
    context = {'latest_review_list':latest_review_list}
    return render(request, 'review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review_detail.html', {'review': review})


def events_list(request):
    events_list = events.objects.order_by('-name')
    context = {'events_list':events_list}
    return render(request, 'events_list.html', context)


def events_detail(request, events_id):
    events = get_object_or_404(events, pk=events_id)
    form = ReviewForm()
    return render(request, 'events_detail.html', {'events': events, 'form': form})

@login_required
def add_review(request, events_id):
    events = get_object_or_404(events, pk=events_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.business = events
        review.user_id = user_name
        review.rating = rating
        review.comment = comment
        review.date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('events:events_detail', args=(events.id,)))

    return render(request, 'events/events_detail.html', {'events': events, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):

    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('events')
    user_reviews_events_ids = set(map(lambda x: x.events.id, user_reviews))

    # get request user cluster name (just the first one righ now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    # get usernames for other memebers of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users, excluding eventss reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(events__id__in=user_reviews_events_ids)
    other_users_reviews_events_ids = set(map(lambda x: x.events.id, other_users_reviews))

    # then get a events list including the previous IDs, order by rating
    events_list = sorted(
        list(events.objects.filter(id__in=other_users_reviews_events_ids)),
        key=lambda x: x.average_rating,
        reverse=True
    )

    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(events_list,6, request=request)
    all_events = p.page(page)
    return render(
        request,
        'dashboard-mylisting.html',
        {'my_all_events': all_events}
    )



from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404,HttpResponse
from .models import events
from .forms import NewEventForm
#from operation.models import UserEvent
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import json
from geopy.geocoders import Nominatim
from catalog.models import UserProfile

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect


from utils.mixin_utils import LoginRequiredMixin
from django.views.generic.base import View
class AllMyEventsListingView(View):


    def get(self,request):

        print(request.user.email)
        myevents=events.objects.filter(founder=request.user.id)
        print(myevents)


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(myevents,6, request=request)

        #print('tesdt')

        all_events = p.page(page)

        return render(request, 'dashboard-mylisting.html', {
            "my_all_events": all_events})




class MySinleEventView( View):
    def get(self,request,event_id):
        event=events.objects.get(id=int(event_id))

        return render(request,'dashboard-myeventdetail.html',{'event':event})




class AddEventView(View):
    def get(self,request):
        return render(request, "dashboard-addevent.html",{})

    def post(self,request):
        if request.method == 'POST':
            event_form = NewEventForm(request.POST)
        #    print("1111111111111111111111")
        #    print(request.user.email)
        # if event_form.is_valid():

            #user=UserProfile.objects.filter(user=request.user)
        #    print("xxxxxxxxxxx")
            event=events()
            event.name=request.POST.get("title", "")
            event.keyword=request.POST.get("keyword", "")
            event.description=request.POST.get("description", "")
            event.city=request.POST.get("city", "")
            event.state = request.POST.get("state", "")
            event.address = request.POST.get('address', '')
            event.founder=request.user.id
        #    geolocator = Nominatim(user_agent="events")
            print(event)


        #    location = geolocator.geocode(request.POST.get("address", "")+','+request.POST.get("city", "")+','+request.POST.get("state", ""))


    #        lat = location.latitude
    #        long = location.longitude

    #        print(lat)
    #        print(long)

    #        event.latitude=lat
    #        event.longitude=long


            event.save()

            #user_event=UserEvent()

            #user_event.user=request.user
            #user_event.event = event

            #user_event.save()

            return HttpResponseRedirect('/mylisting/')
        else:
            return render(request,"index.html")



class HomeEvents(View):
    pass


class EventDetailView(LoginRequiredMixin, View):
    def get(self,request,myevent_id):
        event = get_object_or_404(events, id=myevent_id)
        print("get")
        #print("进了GET 的表")
        return render(request, "dashboard-addevent.html", {"my_event": event})


    def post(self,request,myevent_id):

        title = request.POST.get("title", "")
        keyword = request.POST.get("keyword", "")
        description = request.POST.get("description", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        address = request.POST.get("address", "")

        print("post")
        events.objects.filter(id=myevent_id).update(name=title,keyword=keyword,
                                                   description=description,city=city,
                                                   state=state,address=address)

        # myevents=Event.objects.filter(founder=request.user.id)
        #
        # try:
        #     page = request.GET.get('page', 1)
        # except PageNotAnInteger:
        #     page = 1
        #     # 这里指从allorg中取五个出来，每页显示5个
        # p = Paginator(myevents,6, request=request)
        #
        # all_events = p.page(page)


        return HttpResponseRedirect('/mylisting/')



class ShowAllEventsView(View):
    def get(self,request):

        title=request.GET.get("title","")
        keyword=request.GET.get("keyword","")
        city=request.GET.get("city","")

        #
        # geolocator = Nominatim()
        #
        # location = geolocator.geocode(city)
        #
        # city_lat = location.latitude
        # city_long = location.longitude
        #


        if(title != ""):
            allEvents=events.objects.filter(name__icontains=title)
        else:
            allEvents=events.objects.filter(city=city).union(events.objects.filter(keyword=keyword)).order_by('name')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从allorg中取五个出来，每页显示5个


        #new_all_events=json.dumps([[evt.id,evt.keyword,0,evt.description,evt.address,evt.city,evt.state,
        #                        evt.founder,evt.postal_code,evt.review_count,evt.latitude,evt.longitude,0]
        #                       for evt in allEvents])

        #print(new_all_events)


        p = Paginator(allEvents, 6, request=request)

        all_events = p.page(page)


        # return render(request, "te.html",{"events_json":new_all_events,"lat":city_lat,"long":city_long})

        return render(request, "searchresutls.html", {"searchevents": all_events,
                                                      "keyword": keyword, "city": city})



def deleteevent(request,myevent_id):

    event=get_object_or_404(events,id=myevent_id)
    event.delete()
    return HttpResponseRedirect('/mylisting/')
