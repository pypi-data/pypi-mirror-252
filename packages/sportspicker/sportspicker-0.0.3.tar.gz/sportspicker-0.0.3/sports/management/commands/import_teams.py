from __future__ import unicode_literals

import csv
import random
from os import rename
import importlib



from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = """Loads Participants from a csv file and creates Club based on parsed file name with Participants"""

    def add_arguments(self, parser):
        parser.add_argument('sport', nargs='+', type=str)

    def handle(self, *args, **options):
        sport = options['sport']
        for i in sport:
            mod = (str(i).split(':'))
            package = 'sportspicker-' + mod[0]
            mymod = importlib.import_module(mod[1] + '.utils', package=package)
            print(mymod.import_teams(sport_name=mod[0].title(), league_name=mod[1].title(), verbose=True, force=True))