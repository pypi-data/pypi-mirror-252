from __future__ import unicode_literals

import csv
import random
from os import rename
import importlib



from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from django.contrib.auth import authenticate

from sports.models import Sport, Season, Team, Player, Game, GamePeriod, League, Venue, Division, Broadcast

class Command(BaseCommand):
    help = """Loads Participants from a csv file and creates Club based on parsed file name with Participants"""

    def handle(self, *args, **options):
       Game.objects.all().delete()
       GamePeriod.objects.all().delete()
       # Sport.objects.all().delete()
       # Player.objects.all().delete()
       # Season.objects.all().delete()
       # League.objects.all().delete()
       # Team.objects.all().delete()
       # Venue.objects.all().delete()
       # Division.objects.all().delete()
       # Broadcast.objects.all().delete()