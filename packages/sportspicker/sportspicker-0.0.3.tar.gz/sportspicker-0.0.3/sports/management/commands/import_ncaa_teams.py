# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
from argparse import Namespace
from django.core.management.base import BaseCommand

from ...models import Conference, Division, Team, Venue


class Command(BaseCommand):
    help = """Loads NCAA season data from JSON."""

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    @classmethod
    def process_teams(cls, team_list, conference, division=None):
        """
        Creates teams and their venues.
        """
        for team in team_list:
            # Venue
            if getattr(team, 'venue', False):
                venue_obj, created = Venue.objects.update_or_create(
                    venue_id=team.venue.id, defaults={
                        'name': getattr(team.venue, 'name', ''),
                        'country': getattr(team.venue, 'country', ''),
                        'city': getattr(team.venue, 'city', ''),
                        'state': getattr(team.venue, 'state', ''),
                        'zip_code': getattr(team.venue, 'zip_code', ''),
                    }
                )
                print('{0} venue: {1}'.format('Created' if created else 'Updated', venue_obj))
            else:
                venue_obj = None

            # Team
            team_obj, created = Team.objects.update_or_create(
                team_id=team.id, defaults={
                    'name': team.name,
                    'market': team.market,
                    'conference': conference,
                    'division': division,
                    'venue': venue_obj,
                }
            )
            print('{0} team: {1}'.format('Created' if created else 'Updated', team_obj))

    @classmethod
    def process_conferences(cls, conference_list):
        """
        Creates conferences and divisions (if any) as well as teams and venues
        (via process_teams)
        """
        for conference in conference_list:
            # Conference
            conference_obj, created = Conference.objects.update_or_create(
                conference_id=conference.id, defaults={
                    'name': conference.name
                }
            )
            print('{0} conference: {1}'.format('Created' if created else 'Updated', conference_obj))

            # print(conference.subdivisions[0].id)
            if getattr(conference, 'subdivisions', False):
                for division in conference.subdivisions:
                    # Division
                    division_obj, created = Division.objects.update_or_create(
                        division_id=division.id, defaults={
                            'name': division.name,
                            'conference': conference_obj,
                        }
                    )
                    print('{0} division: {1}'.format('Created' if created else 'Updated', division_obj))
                    cls.process_teams(division.teams, conference_obj, division_obj)
            elif getattr(conference, 'teams', None):
                cls.process_teams(conference.teams, conference_obj)
            else:
                pass

    def handle(self, *args, **options):
        file_name = options['file_name'][0]
        file_json = open(file_name).read()
        data = json.loads(file_json, object_hook=lambda d: Namespace(**d))

        self.process_conferences(data.conferences)
