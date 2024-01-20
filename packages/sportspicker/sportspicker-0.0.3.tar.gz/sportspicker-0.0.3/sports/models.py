# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import timedelta
from json import loads

from django.urls import reverse
from django.db import models
from django.template.defaultfilters import date as date_format
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.utils import timezone

import requests


class Sport(models.Model):
    name = models.CharField(_('Sport Name'), max_length=40, blank=False, default='')
    # api_key = models.CharField(_('API Key'), max_length=40, blank=False, default='')

    class Meta(object):
        verbose_name = _('Sport')
        verbose_name_plural = _('Sports')
        app_label = 'sports'

    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(_('League Name'), max_length=40, blank=False, default='')
    sport = models.ForeignKey('sports.Sport', related_name='leagues', verbose_name=_('Sport'),
                                   on_delete=models.CASCADE)
    # api_key = models.CharField(_('API Key'), max_length=40, blank=False, default='')

    class Meta(object):
        verbose_name = _('League')
        verbose_name_plural = _('Leagues')
        app_label = 'sports'

    def __str__(self):
        return self.name

class Conference(models.Model):
    conference_id = models.CharField(_('conference ID'), max_length=40, blank=False, default='')
    name = models.CharField(_('name'), max_length=64, blank=False, default='')
    league = models.ForeignKey('sports.League', related_name='conferences', verbose_name=_('League'),
                                   on_delete=models.CASCADE)
    class Meta(object):
        verbose_name = _('conference')
        verbose_name_plural = _('conferences')
        app_label = 'sports'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sports:conference_detail', args=[self.pk, ])


class Division(models.Model):
    division_id = models.CharField(_('division ID'), max_length=40, blank=False, default='')
    name = models.CharField(_('name'), max_length=32, blank=False, default='')

    conference = models.ForeignKey('sports.Conference', related_name='divisions', verbose_name=_('conference'),
                                   on_delete=models.CASCADE)

    class Meta(object):
        verbose_name = _('division')
        verbose_name_plural = _('divisions')
        app_label = 'sports'

    def __str__(self):
        return self.name


class Venue(models.Model):
    venue_id = models.CharField(_('venue ID'), max_length=40, blank=False, null=False)
    name = models.CharField(_('name'), max_length=128, blank=False, null=False)
    address = models.CharField(_('address'), max_length=128, blank=True, null=True, default=None)
    country = models.CharField(_('country'), max_length=32, blank=True, null=True, default=None)
    city = models.CharField(_('city'), max_length=32, blank=True, null=True, default=None)
    state = models.CharField(_('state'), max_length=32, blank=True, null=True, default=None)
    zip_code = models.CharField(_('ZIP Code'), max_length=10, blank=True, null=True, default=None)

    class Meta(object):
        verbose_name = _('venue')
        verbose_name_plural = _('venues')
        app_label = 'sports'

    def __str__(self):
        # TOTAL HACK
        # Note, this is replacing a unicode long-dash with an ASCII-dash.
        return self.name.replace('–', '-')


class Team(models.Model):
    team_id = models.CharField(_('team ID'), max_length=40, blank=False, default='')
    name = models.CharField(_('name'), max_length=64, blank=True, default='')
    alias = models.CharField(_('alias'), max_length=64, blank=True, default='')
    market = models.CharField(_('market'), max_length=64, blank=True, default='')
    conference = models.ForeignKey('sports.Conference', related_name='teams', verbose_name=_('conference'), null=True, on_delete=models.SET_NULL)
    division = models.ForeignKey('sports.Division', related_name='teams', verbose_name=_('division'), null=True, on_delete=models.SET_NULL)
    venue = models.ForeignKey('sports.Venue', related_name='teams', verbose_name=_('venue'), null=True, on_delete=models.SET_NULL)

    class Meta(object):
        verbose_name = _('team')
        verbose_name_plural = _('teams')
        ordering = ('name', 'division', 'conference',)
        app_label = 'sports'

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('sports:team_detail', args=[self.pk, ])

    @property
    def short_name(self):
        return self.name

    @property
    def full_name(self):
        return '{0} {1}'.format(self.market, self.name)


class Player(models.Model):
    player_id = models.CharField(max_length=40)
    first_name = models.CharField(_('first name'), max_length=255, blank=False)
    last_name = models.CharField(_('last name'), max_length=255, blank=False)
    team = models.ForeignKey('sports.Team', on_delete=models.CASCADE)
    jersey_number = models.CharField(_('jersey number'), max_length=10, blank=True, null=True)
    height = models.CharField(_('height'), max_length=10, blank=True, null=True)
    weight = models.CharField(_('weight'), max_length=10, blank=True, null=True)
    position = models.CharField(_('position'), max_length=10, blank=True, null=True)
    primary_position = models.CharField(_('primary position'), max_length=10, blank=True, null=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)


    class Meta(object):
        verbose_name = _('Player')
        verbose_name_plural = _('Players')
        ordering = ('team', 'last_name', 'first_name',)
        app_label = 'sports'

    def __str__(self):
        return '{first} {last}, {team}'.format(first=self.first_name, last=self.last_name, team=self.team.name)

class Season(models.Model):


    # User Editable Label.
    label = models.CharField(_('label'), max_length=100, blank=True, default=None, null=True)
    season_id = models.CharField(_('season id'), max_length=40, blank=False)
    # These two fields are used to match against the remote api
    name = models.CharField(_('name'), max_length=32, blank=False, default='')
    type = models.CharField(_('type'), max_length=32, blank=False, default='')
    year = models.CharField(_('year'), max_length=4, blank=False, default='')
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('end date'), blank=True, null=True)
    league = models.ForeignKey('sports.League', related_name='seasons', verbose_name=_('League'),
                                   on_delete=models.CASCADE)
    # JSON Hash to reduce lookups
    hash = models.CharField(_('hash'), max_length=32, blank=True, null=True)
    class Meta(object):
        verbose_name = _('season')
        verbose_name_plural = _('seasons')
        app_label = 'sports'

    def __str__(self):
        return self.label if self.label else self.name


class GamePeriod(models.Model):
    label = models.CharField(_('label'), max_length=100, blank=True, default=None, null=True)
    period_id = models.CharField(_('game period ID'), max_length=40, blank=True, null=True)
    # TODO: Explore converting this to a PositiveSmallIntegerField
    number = models.PositiveSmallIntegerField(_('number'), blank=False, default=0)
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('end date'), blank=True, null=True)
    season = models.ForeignKey('sports.Season', related_name='game_periods', verbose_name=_('season'), blank=True,
                               null=True, on_delete=models.SET_NULL)

    class Meta(object):
        verbose_name = _('game period')
        verbose_name_plural = _('game periods')
        ordering = ('season', 'number',)
        app_label = 'sports'

    @property
    def earliest_game_start(self):
        try:
            return self.games.filter(scheduled__isnull=False).earliest('scheduled').scheduled
        except Game.DoesNotExist:
            return None

    @property
    def latest_game_start(self):
        try:
            return self.games.filter(scheduled__isnull=False).latest('scheduled').scheduled
        except Game.DoesNotExist:
            return None

    @property
    def default_deadline(self):
        try:
            return (self.earliest_game_start - timedelta(days=1)).replace(hour=23, minute=59)
        except TypeError:
            return None

    @property
    def default_expert_deadline(self):
        try:
            return (self.earliest_game_start - timedelta(days=1)).replace(hour=18, minute=00)
        except TypeError:
            return None

    def __str__(self):
        return '{0}: Game:{1}'.format(self.season, self.number)


class Game(models.Model):
    game_id = models.CharField(_('game ID'), max_length=40, blank=False, default='')
    game_period = models.ForeignKey('sports.GamePeriod', related_name='games', verbose_name=_('game period'), null=True, on_delete=models.SET_NULL)
    scheduled = models.DateTimeField(_('scheduled'))
    scored = models.DateTimeField(_('scored'), blank=True, null=True)
    summary = models.TextField(_('summary'), blank=True, null=True)
    coverage = models.CharField(_('coverage'), max_length=32, blank=True, default='')
    home_rotation = models.CharField(_('home rotation'), max_length=32, blank=True, default='')
    away_rotation = models.CharField(_('away rotation'), max_length=32, blank=True, default='')
    home = models.ForeignKey('sports.Team', related_name='game_home', on_delete=models.CASCADE)
    away = models.ForeignKey('sports.Team', related_name='game_away', on_delete=models.CASCADE)
    status = models.CharField(_('status'), max_length=32, blank=True, default='')
    venue = models.ForeignKey('sports.Venue', related_name='games', verbose_name=_('venue'), null=True, on_delete=models.SET_NULL)
    home_points = models.PositiveSmallIntegerField(_('home points'), blank=True, null=True)
    away_points = models.PositiveSmallIntegerField(_('away points'), blank=True, null=True)

    class Meta(object):
        verbose_name = _('game')
        verbose_name_plural = _('games')
        ordering = ['scheduled', ]
        app_label = 'sports'

    def __str__(self):
        # return '{o.away} at {o.home}'.format(o=self)
        return self.full_name_with_date

    def get_absolute_url(self):
        # Returns the "sportsadmin" URL for this game
        return reverse('sports:game_detail', args=[self.pk, ])

    def save(self, **kwargs):
        """
        Ensure that `scored` is set to None if there are no scores and a
        timestamp (or leave as the provided non-None value) if they are set.
        """
        if self.home_points is None and self.away_points is None:
            self.scored = None
        elif self.scored is None:
            self.scored = timezone.now()
        super(Game, self).save(**kwargs)

    @property
    def name(self):
        return '{o.away} at {o.home}'.format(o=self)

    @property
    def game_date(self):
        return date_format(self.scheduled)

    @property
    def short_name(self):
        return '{o.away.short_name} at {o.home.short_name}'.format(o=self)

    @property
    def full_name(self):
        return '{o.away.full_name} at {o.home.full_name}'.format(o=self)

    @property
    def markets_name(self):
        return '{o.away.market} at {o.home.market}'.format(o=self)

    @property
    def full_name_with_date(self):
        return '{o.away.full_name} at {o.home.full_name} ({o.game_date})'.format(o=self)

    @property
    def game_period_name(self):
        return '{o.game_period.number}'.format(o=self)

    @property
    def season_name(self):
        return '{o.game_period.season.season_name}'.format(o=self)

    def get_winner(self):
        if self.is_scored():
            if self.home_points > self.away_points:
                return self.home
            elif self.away_points > self.home_points:
                return self.away
        return None

    def pull_score(self, api_key, format='json'):
        # TODO need to adapt for both NFL and NCAA
        if self.scored is None:
            api_call = 'http(s)://api.sportradar.us/ncaafb-[access_level][version]/[year]/[ncaafb_season]/' \
                       '[ncaafb_season_week]/[away_team]/[home_team]/summary.[format]?api_key=[your_api_key]'
            api_call = api_call.replace('(s)', '')
            season = self.game_period.season
            api_call = api_call.replace('[year]', season.season_name)
            api_call = api_call.replace('[ncaafb_season]', season.season_type)
            api_call = api_call.replace('[ncaafb_season_week]', str(self.game_period.number))
            if 'ncaafb' in api_call:
                api_call = api_call.replace('[access_level][version]', 't1')
            elif 'nfl' in api_call:
                api_call = api_call.replace('[access_level][version]', 'ot1')
            api_call = api_call.replace('[away_team]', self.away.team_id)
            api_call = api_call.replace('[home_team]', self.home.team_id)
            api_call = api_call.replace('[format]', format)
            api_call = api_call.replace('[your_api_key]', api_key)
            result = loads(self.send_request(api_call))
            if (result['status']) == 'closed':
                self.away_points = (result['away_team'])['points']
                self.home_points = (result['home_team'])['points']
                self.summary = result
                self.scored = timezone.now()

                self.save()
                return '{o.away.full_name} {o.away_points}, {o.home.full_name} {o.home_points}'.format(o=self)
            elif (result['status']) == 'complete':
                return 'Game Complete, Scores Being Finalized: {o.away.full_name} at {o.home.full_name}'.format(o=self)
            else:
                return 'Game In Progress: {o.away.full_name} at {o.home.full_name}'.format(o=self)
        else:
            return 'Already Scored on {o.scored}: {o.away.full_name} {o.away_points}, {o.home.full_name} ' \
                   '{o.home_points}'.format(o=self)

    def send_request(self, url):
        try:
            response = requests.get(url=url)
            return smart_str(response.text)
        except requests.exceptions.RequestException:
            raise

    def is_scored(self):
        return not (self.scored is None)


class Broadcast(models.Model):
    broadcast_type = models.CharField(_('type'), max_length=40, blank=False, default='')
    broadcast_address = models.CharField(_('address'), max_length=64, blank=False, default='')
    game = models.ForeignKey('sports.Game', verbose_name=_('game'), on_delete=models.CASCADE)

    class Meta(object):
        verbose_name = _('broadcast')
        verbose_name_plural = _('broadcasts')
        app_label = 'sports'

    def __str__(self):
        return '{o.broadcast_type}:{o.broadcast_address}'.format(o=self)


class GameSummary(models.Model):
    game = models.ForeignKey('sports.Game', related_name='game', on_delete=models.CASCADE)
    home_points = models.PositiveSmallIntegerField(_('home points'), blank=False, default=0)
    away_points = models.PositiveSmallIntegerField(_('away points'), blank=False, default=0)

    class Meta(object):
        verbose_name = _('summary')
        verbose_name_plural = _('summaries')
        app_label = 'sports'
