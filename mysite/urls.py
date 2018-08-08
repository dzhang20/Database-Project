"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

from django.contrib import admin
from django.urls import path

from events import views
from django.views.generic import TemplateView
from catalog.views import LoginView,RegisterView,LogoutView
from events.views import AddEventView,AllMyEventsListingView,EventDetailView,ShowAllEventsView
urlpatterns = [

    path('admin/', admin.site.urls),
    path('catalog', include('catalog.urls')),
    path('events/',include(('events.urls','events'),namespace="events")),
    path('accounts/', include('registration.backends.simple.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('django.contrib.auth.urls','auth'), namespace="auth")),
    path('chat/', include('wechat.urls')),

    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),

    path("mylisting/", AllMyEventsListingView.as_view(), name="mylisting"),
    path('recommendation/',views.user_recommendation_list, name='recommendation'),
    path("addevent/", AddEventView.as_view(), name="addevent"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("mysingleevent/", TemplateView.as_view(template_name="myprofile.html"), name="myprofile"),

    path("updateevent/<myevent_id>/", EventDetailView.as_view(), name='updateevent'),
    path("delete/<myevent_id>/", views.deleteevent, name='delete'),
    path("searchresults/", ShowAllEventsView.as_view(), name='searchresults'),

#    path('listingevents/', views.showlisting, name='dashboard-listing-table'),
#    path('delete/<id>/', views.deleteevent, name='delete'),
#    path('searchevent/', views.searchevent, name = 'search'),
##    path('updateevent/<id>/', views.updateevent, name='update'),


#    url(r'^accounts/', include('registration.backends.simple.urls')),
#    url(r'^accounts/', include('django.contrib.auth.urls')),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/')),
]
urlpatterns += staticfiles_urlpatterns()
