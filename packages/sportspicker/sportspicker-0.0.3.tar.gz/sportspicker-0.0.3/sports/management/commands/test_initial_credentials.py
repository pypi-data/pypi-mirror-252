# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from .import_club import Command as ClubCommand

from sportspicker.models import Club, ClubUser


class Command(BaseCommand):
    help = """Tests each user in a Club with the expected, initial generated username and password"""

    def add_arguments(self, parser):
        parser.add_argument('club_name', nargs='+', type=str)

    def handle(self, *args, **options):
        club_name = options['club_name'][0]
        club = Club.objects.get(slug=club_name)

        for x in ClubUser.objects.filter(club=club):
            generated_password = ClubCommand.generate_password(
                fname=x.user.first_name, lname=x.user.last_name, cname=club.name, method='last_name'
            )
            result = authenticate(username=x.user.username, password=generated_password)
            if result is not None:
                print 'User ' + str(x.user.username) + ' successfully logged in with password ' + generated_password
            else:
                print 'Error: User ' + str(x.user.username) + ' failed to log in with password ' + generated_password