# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
from argparse import Namespace
from dateutil.parser import parse

from django.core.management.base import BaseCommand
from django.utils.lru_cache import lru_cache

from ...models import Broadcast, Game, GamePeriod, Season, Team, Venue


class Command(BaseCommand):
    help = """Loads NFL Game Period data from JSON."""

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        file_name = options['file_name'][0]
        file_json = open(file_name).read()

        season = json.loads(file_json, object_hook=lambda d: Namespace(**d))
        season_obj, _ = Season.objects.get_or_create(
            season_name=season.year, season_type=season.type, label=self.derive_label_from_file_name(file_name))

        for game_period in season.weeks:
            game_period_obj, created = GamePeriod.objects.update_or_create(
                sport_radar_period_id=game_period.id, defaults={'number': game_period.sequence, 'season': season_obj})
            self.process_games(game_period.games, game_period_obj)

    @classmethod
    def derive_label_from_file_name(cls, file_name):
        try:
            file_name = (((file_name.split('/'))[-1]).split('.')[0]).replace('-', ' ')
            file_name = file_name.replace(' games', '')
            return file_name
        except:
            return file_name

    @classmethod
    def get_venue_from_parent(cls, parent):
        """
        Attempts to extract a Venue object from the given «obj». If one is
        found, update or create the venue and return the resulting object.
        Otherwise, return None.

        :return: Venue or None
        :rtype: Venue or None
        """
        venue = getattr(parent, 'venue', None)
        if not venue:
            return None

        venue_obj, created = Venue.objects.update_or_create(
            venue_id=venue.id, defaults={
                'name': venue.name,
                'country': getattr(venue, 'country', ''),
                'city': getattr(venue, 'city', ''),
                'state': getattr(venue, 'state', ''),
                'zip_code': getattr(venue, 'zip', ''),
            }
        )
        print('{0} venue: {1}'.format('Created' if created else 'Updated', venue_obj))
        return venue_obj

    @classmethod
    @lru_cache()
    def team_from_id(cls, team_id):
        team_obj, created = Team.objects.get_or_create(team_id=team_id)
        if created:
            team_obj.name = team_id
            team_obj.save()
            print('{0} team: {1}'.format('Created' if created else 'Updated', team_obj))
        return team_obj

    @classmethod
    def process_games(cls, game_list, game_period_obj):
        deleteable_broadcast_ids = []
        for game in game_list:
            game_obj, created = Game.objects.update_or_create(
                game_id=game.id, defaults={
                    'game_period': game_period_obj,
                    'scheduled': parse(game.scheduled),
                    'home': cls.team_from_id(game.home.id),
                    'away': cls.team_from_id(game.away.id),
                    'status': game.status,
                    'venue': cls.get_venue_from_parent(game),
                }
            )

            if getattr(game, 'broadcast', False):
                # Creates new Broadcast objects as required
                broadcast_ids = []
                for broadcast_type, broadcast_address in game.broadcast.__dict__.items():
                    broadcast_obj, created = Broadcast.objects.get_or_create(
                        game_id=game_obj.pk, broadcast_type=broadcast_type,
                        broadcast_address=broadcast_address)
                    broadcast_ids.append(broadcast_obj.pk)
            else:
                broadcast_ids = []

            # Which broadcast objects for this game, if any, can be deleted?
            deleteable_broadcast_ids.extend(Broadcast.objects.exclude(id__in=broadcast_ids)
                                                             .filter(game_id=game_obj.pk)
                                                             .values_list('pk', flat=True))
        # Now, delete all the unused broadcast objects in one go
        Broadcast.objects.filter(id__in=deleteable_broadcast_ids).delete()
