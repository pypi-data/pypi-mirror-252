# # -*- coding: utf-8 -*-
#
# from __future__ import unicode_literals
#
# from django.conf.urls import url
#
# from .views import (
#     ConferenceListView,
#     ConferenceDetailView,
#     GameDetailView,
#     TeamDetailView,
# )
#
#
# urlpatterns = [
#     url(r'^$',
#         ConferenceListView.as_view(), name='conference_list'),
#
#     url(r'^(?P<conference_pk>\d+)/$',
#         ConferenceDetailView.as_view(), name='conference_detail'),
#
#     url(r'^(?P<conference_pk>\d+)/team-(?P<team_pk>[-\w]+)/$',
#         TeamDetailView.as_view(), name='team_detail'),
#
#     url(r'^games/game-(?P<game_pk>\d+)/$',
#         GameDetailView.as_view(), name='game_detail'),
# ]
"""
URL configuration for sportspicker project.

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

from django.urls import path, include

# urlpatterns = [
#
#     path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
# ]

