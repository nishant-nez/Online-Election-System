"""
URL configuration for online_election_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from elections import views as election_views

urlpatterns = [
    path('', include('dashboard.urls')),
    path('elections/', election_views.home, name='elections_home'),
    path('elections/<int:pk>/', election_views.election_detail, name='election_detail'),
    path('elections/<int:pk>/candidates/', election_views.election_candidates, name='election_candidates'),
    path('candidate/<int:pk>/', election_views.candidate_detail, name='candidate_detail'),
    path('vote/<int:pk>/', election_views.confirm_vote, name='confirm_vote'),
    path('vote/delete/<int:pk>/', election_views.confirm_vote_delete, name='confirm_vote_delete'),
    path('candidates/', election_views.candidates, name='candidates'),
    path('history/', election_views.vote_history, name='vote_history'),
    # new admin
    path('admin/', include('administration.urls')),
    # old admin
    path('oldadmin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    # election stats
    path('stats/<int:pk>', election_views.election_stats, name='election_stats'),
    path('__reload__/', include('django_browser_reload.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
