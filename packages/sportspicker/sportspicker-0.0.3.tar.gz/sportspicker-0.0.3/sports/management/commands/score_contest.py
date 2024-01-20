# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime, timedelta
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from sportspicker.models import Club, Contest, LeaderboardPluginModel


class Command(BaseCommand):
    help = """Scores games for a specified Contest"""

    def add_arguments(self, parser):
        parser.add_argument('contest_name', nargs='+', type=str)
        parser.add_argument('api_key', nargs='+', type=str)
        parser.add_argument('--recache', dest='recache', action='store_true')

    def handle(self, *args, **options):
        contest_name = options['contest_name'][0]
        api_key = options['api_key'][0]
        recache = options['recache'] == True
        contest = Contest.objects.get(slug=contest_name)
        cutoff = timezone.now() - timedelta(minutes=200)
        for period in contest.contest_periods.filter(start_date__lte=cutoff):
            for game in period.games.filter(scheduled__lte=cutoff):
                if not game.scored:
                    print game.pull_score(api_key)
                if game.scored and recache:
                    self.re_cache_leaderboards(game)
                sleep(1)

    def re_cache_leaderboards(self, game):
        """
        Recache all the leaderboards for this game.
        """
        for club in Club.objects.filter(contests__games=game):
            club_ids = [club.pk, ]
            for contest in club.contests.filter(games=game):
                for contest_period in contest.contest_periods.filter(games=game):
                    LeaderboardPluginModel.get_leaderboard(club_ids, scope=contest_period, recache=True)
                LeaderboardPluginModel.get_leaderboard(club_ids, scope=contest, recache=True)
            LeaderboardPluginModel.get_leaderboard(club_ids, scope=club, recache=True)
