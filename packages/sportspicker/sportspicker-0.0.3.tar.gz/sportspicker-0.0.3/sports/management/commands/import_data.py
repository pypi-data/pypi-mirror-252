# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import os
import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.encoding import smart_str


class Command(BaseCommand):
    help = """Pulls data from sportsradar API."""
    season_config = {}

    global_values = {
        'ncaa-divisions': ['FBS', 'FCS', 'D2', 'D3', 'NAIA', 'USCAA'],
        'types': ['teams', 'games']
    }
    season_config['Global'] = global_values

    # NCAA Config - move this to a settings file eventually
    ncaa_config = {
        'api_key': 'g56be5vwvehput2zr3fjmejg',
        'format': 'json',
        'access_level': 't',
        'division': ['FBS', 'FCS', 'D2', 'D3',  'NAIA', 'USCAA'],
        'version': '1',
        'https': True,
    }
    action_urls = {}

    # specify the exact API url as listed in the SportRadar docs, along with
    # guide in comments below.
    # http://developer.sportradar.us/docs/NCAA_Football_API

    # Grab Teams
    action_urls.update({
        'teams':
        'http(s)://api.sportradar.us/ncaafb-[access_level][version]/teams/[division]/hierarchy.[format]'
        '?api_key=[your_api_key]'
    })

    # [access_level] = Real - Time(rt), Premium(p), Standard(s), Basic(b), Trial(t)
    # [version] = whole number(sequential, starting with the number 1)
    # [division] = FBS, FCS, D2, D3, NAIA or USCAA
    # [format] = xml, json

    # Grab Games
    action_urls.update({
        'games':
        'http(s)://api.sportradar.us/ncaafb-[access_level][version]/[year]/[ncaafb_season]/schedule.[format]'
        '?api_key=[your_api_key]'
    })

    # [access_level] = Real - Time(rt), Premium(p), Standard(s), Basic(b), Trial(t)
    # [version] = whole number(sequential, starting with the number 1)
    # [year] = yyyy
    # [ncaafb_season] = Regular Season(REG), Postseason(PST) - Note: PST used
    #                   for seasons 2012 and prior
    # [format] = xml, json

    ncaa_config.update({'action_urls': action_urls})
    season_config['NCAA-Reg'] = ncaa_config

    # NFL Config - move this to a settings file eventually
    nfl_config = {
        'api_key': 'dj2c5dpkcq6c9z6k38btaarr',
        'format': 'json',
        'access_level': 't',
        'division': ['FBS', 'FCS', 'D2', 'D3',  'NAIA', 'USCAA'],
        'version': '1',
        'https': True,
    }
    action_urls = {}

    # specify the exact API url as listed in the SportRadar docs, along with
    # guide in comments below.
    # http://developer.sportradar.us/docs/NCAA_Football_API

    # Grab Teams
    action_urls.update({
        'teams':
        'http(s)://api.sportradar.us/ncaafb-[access_level][version]/teams/[division]/hierarchy.[format]'
        '?api_key=[your_api_key]'
    })

    # [access_level] = Real - Time(rt), Premium(p), Standard(s), Basic(b), Trial(t)
    # [version] = whole number(sequential, starting with the number 1)
    # [division] = FBS, FCS, D2, D3, NAIA or USCAA
    # [format] = xml, json

    # Grab Games
    action_urls.update({
        'games':
        'http(s)://api.sportradar.us/ncaafb-[access_level][version]/[year]/[ncaafb_season]/schedule.[format]'
        '?api_key=[your_api_key]'
    })

    # [access_level] = Real - Time(rt), Premium(p), Standard(s), Basic(b), Trial(t)
    # [version] = whole number(sequential, starting with the number 1)
    # [year] = yyyy
    # [ncaafb_season] = Regular Season(REG), Postseason(PST) - Note: PST used
    #                   for seasons 2012 and prior
    # [format] = xml, json

    ncaa_config.update({'action_urls': action_urls})
    season_config['NCAA-Reg'] = ncaa_config

    def add_arguments(self, parser):
        # allow pulling of previous years for testing
        years = range(2012, datetime.datetime.now().year + 1)
        division = ['FBS', 'FCS', 'D2', 'D3',  'NAIA', 'USCAA']
        choices = self.season_config.keys()
        parser.add_argument('season', nargs='+', type=str, help='The Season, eg NFL or NCAA', choices=choices)
        parser.add_argument('year', nargs='+', type=int, help='The Year, eg 2016', choices=years)
        parser.add_argument('division', nargs='+', type=str, help='The Division, eg. FSB', choices=division)
        parser.add_argument('type', nargs='+', type=str, help='The Year, eg 2016', choices=('teams','games'))

    def handle(self, *args, **options):
        season = str(options['season'][0])
        year = str(options['year'][0])
        division = str(options['division'][0])
        season_type = str(options['type'][0])
        data_format = str(self.season_config[season]['format'])

        # Generate the filename from the season, year, division and type, in
        # preferred format
        file_name = "{season}-{year}-{division}-{season_type}.{data_format}".format(
            season=season,
            year=year,
            division=division,
            season_type=season_type,
            data_format=data_format,
        )
        url = self.get_request_url(
            config=self.season_config,
            season=season,
            year=year,
            division=division,
            season_type=season_type,
        )

        # send the request and receive the response in text format
        response = self.send_request(url)

        # Make sure the data dir, as specified in the default django settings
        # file exists.
        target_dir = "{dir}{year}/{season_type}/".format(
            dir=getattr(settings, 'SPORTSDATADIR', 'data/'),
            year=year,
            season_type=season_type,
        )
        self.ensure_dir(target_dir)
        self.write_response_to_disk(target_dir + file_name, response)
        return url

    @classmethod
    def ensure_dir(cls, f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            os.makedirs(d)

    @classmethod
    def write_response_to_disk(cls, filename, text):
        with open(filename, mode='w') as out_file:
            out_file.write(text)

    @classmethod
    def get_request_url(cls, config, season, year, division, season_type):
        """
        Returns the appropriate URL for the requested data.
        """
        is_https = config[season]['https']
        url = str((config[season]['action_urls'])[season_type])

        placeholders = {
            'http(s)': 'https' if is_https else 'http',
            '[access_level]': str(config[season]['access_level']),
            '[division]': division,
            '[format]': str(config[season]['format']),
            '[ncaafb_season]': season_type,
            '[version]': str(config[season]['version']),
            '[year]': year,
            '[your_api_key]': str(config[season]['api_key']),
        }

        for placeholder, value in placeholders.items():
            if placeholder in url:
                url = url.replace(placeholder, value)

        return url

    @classmethod
    def send_request(cls, url):
        try:
            response = requests.get(url=url)
            return smart_str(response.text)
        except requests.exceptions.RequestException:
            raise
