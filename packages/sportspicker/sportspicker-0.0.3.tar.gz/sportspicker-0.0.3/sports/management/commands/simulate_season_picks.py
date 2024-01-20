# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from random import choice
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import authenticate
from .import_club import Command as ClubCommand

from sportspicker.models import Club, Contest, ClubUser, GamePick


class Command(BaseCommand):
    help = """Simulates a season of picks for a specified club"""

    def add_arguments(self, parser):
        parser.add_argument('club_name', nargs='+', type=str)
        parser.add_argument('contest_name', nargs='+', type=str)

    def handle(self, *args, **options):
        club_name = options['club_name'][0]
        club = Club.objects.get(slug=club_name)
        contest_name = options['contest_name'][0]
        contest = Contest.objects.get(slug=contest_name)

        for x in ClubUser.objects.filter(club=club):

            for pindex, period in enumerate(contest.contest_periods.all()):

                for __, game in enumerate(period.games.all()):

                    choices = (game.away, game.home)
                    if game.pk == period.tie_breaker_game_id:
                        homescore = choice(range(0, 50))
                        visitorscore = choice(range(0, 50))
                    else:
                        homescore = None
                        visitorscore = None
                    guess, created = GamePick.objects.update_or_create(
                        club_user_id=x.pk,
                        game_id=game.pk,
                        defaults={
                            'winner': choice(choices),
                            'home_score': homescore,
                            'visitor_score': visitorscore,
                            'pick_time': timezone.now()
                        }
                    )
                    print guess
