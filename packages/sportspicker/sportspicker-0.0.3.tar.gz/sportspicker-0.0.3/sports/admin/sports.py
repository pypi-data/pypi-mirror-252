# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext as _

from django_select2.forms import Select2Widget

from ..models import Sport, League, Broadcast, Conference, Division, Game, GamePeriod, Season, Team, Player, Venue, GameSummary

from .mixins import ReadOnlyAdminMixin, LinkedFieldsMixin


class BroadcastInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Broadcast
    fields = ('broadcast_type', 'broadcast_address', )
    extra = 0
    show_change_link = True


class DivisionInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Division
    fields = ('name', )
    extra = 0
    readonly_fields = ('name', )
    show_change_link = True


class GameInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Game
    fields = ('scheduled', 'home', 'away', )
    extra = 0
    show_change_link = True


# TODO: Currently, we need to use two "GameInlines" when used on Team. This is
# because Game has two FKs (soon to be 3) that point to Team. At some point,
# we can create a new, custom inline that will re-unify 'home' and 'away' into
# a single inline. Or at least re-label these two so they communicate better.
class HomeGameInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Game
    fk_name = 'home'
    fields = ('scheduled', 'away', )
    extra = 0
    show_change_link = True


class AwayGameInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Game
    fk_name = 'away'
    fields = ('scheduled', 'home', )
    extra = 0
    show_change_link = True


class GamePeriodInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = GamePeriod
    extra = 0
    fields = ('season', 'number', )
    show_change_link = True

    def get_queryset(self, request):
        qs = super(GamePeriodInline, self).get_queryset(request)
        return qs.annotate(num_games=Count('games'))


class TeamInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Team
    extra = 0
    fields = ('name', 'market', 'conference', 'division', )
    readonly_fields = ('name', 'market', 'conference', 'division', )
    show_change_link = True

class LeagueInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = League
    extra = 0
    fields = ('name',)
    readonly_fields = ('name',)
    show_change_link = False

class PlayersInline(ReadOnlyAdminMixin, admin.TabularInline):
    model = Player
    extra = 0
    fields = ('first_name', 'last_name',)
    readonly_fields = ('first_name', 'last_name',)
    show_change_link = False


# ========== INLINES ^ / ADMINS v ==============

class SportAdmin(LinkedFieldsMixin, ReadOnlyAdminMixin, admin.ModelAdmin):
    inlines = (LeagueInline,)

admin.site.register(Sport, SportAdmin)

class LeagueAdmin(LinkedFieldsMixin, ReadOnlyAdminMixin, admin.ModelAdmin):
    # inlines = (DivisionInline,)
    pass

admin.site.register(League, LeagueAdmin)


class BroadcastAdmin(LinkedFieldsMixin, ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('game', 'broadcast_type', 'broadcast_address', )
    list_filter = ('broadcast_type', )
    fields = ('game', 'broadcast_type', 'broadcast_address', )

admin.site.register(Broadcast, BroadcastAdmin)

class GameSummaryAdmin(LinkedFieldsMixin, ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('game', 'away_points', 'home_points', )
    fields = ('game', 'away_points', 'home_points', )

admin.site.register(GameSummary, GameSummaryAdmin)


class ConferenceAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'num_teams', )
    readonly_fields = ('name', 'league', )
    inlines = (DivisionInline, TeamInline, )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'league',
            )
        }),
        (_('Advanced'), {
            'classes': ('collapse', ),
            'fields': (
                'conference_id',
            )
        })
    )

    def get_queryset(self, request):
        qs = super(ConferenceAdmin, self).get_queryset(request)
        return qs.annotate(num_teams=Count('teams'))

    def num_teams(self, obj):
        return obj.num_teams
    num_teams.admin_order_field = 'num_teams'
    num_teams.short_description = '# Teams'

admin.site.register(Conference, ConferenceAdmin)


class DivisionAdmin(LinkedFieldsMixin, ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'conference', 'get_league', 'get_sport', 'num_teams', )
    list_display_links = ('name', )
    inlines = (TeamInline, )
    fieldsets = (
        (None, {
            'fields': (
                'name', 'conference',
            )
        }),
        (_('Advanced'), {
            'classes': ('collapse', ),
            'fields': (
                'division_id',
            )
        })
    )

    def get_queryset(self, request):
        qs = super(DivisionAdmin, self).get_queryset(request)
        return qs.annotate(num_teams=Count('teams'))

    def num_teams(self, obj):
        return obj.num_teams
    num_teams.admin_order_field = 'num_teams'
    num_teams.short_description = '# Teams'
    def get_league(self, obj):
        return obj.conference.league
    get_league.admin_order_field = 'num_teams'
    get_league.short_description = 'League'
    def get_sport(self, obj):
        return obj.conference.league.sport

    get_sport.admin_order_field = 'get_sport'
    get_sport.short_description = 'Sport'

admin.site.register(Division, DivisionAdmin)


class GameAdminForm(forms.ModelForm):
    # home = ModelSelect2Field(queryset=Team.objects.all())
    # away = ModelSelect2Field(queryset=Team.objects.all())
    # venue = ModelSelect2Field(queryset=Venue.objects.all())

    class Meta:
        model = Game
        fields = '__all__'
        widgets = {
            'home': Select2Widget,
            'away': Select2Widget,
            'venue': Select2Widget,
        }

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js',
        )


# LinkedFieldsMixin,
class GameAdmin(admin.ModelAdmin):
    list_display = ('gamesummary', 'scheduled', 'game_period', 'away', 'away_points', 'home', 'home_points', 'venue', )
    inlines = (BroadcastInline, )
    list_filter = ('away', 'scheduled', 'scored', )
    form = GameAdminForm
    ordering = ['-scheduled',]

    def gamesummary(self, obj):
        if obj.scored is not None:
            return '{o.away} {o.away_points}, {o.home.full_name} {o.home_points}'.format(o=obj)
        else:
            return '{o.away} at {o.home.full_name}'.format(o=obj)
    gamesummary.short_description = 'Summary'

    def gameperiod(self, obj):
        return '{o.game_period_name}'.format(o=obj)
    gameperiod.short_description = 'Period'

    def season(self, obj):
        return '{o.season_name}'.format(o=obj)
    season.short_description = 'Year'

admin.site.register(Game, GameAdmin)


# LinkedFieldsMixin, ReadOnlyAdminMixin,
# explicit_readonly_fields = ('earliest_game_start', 'latest_game_start', )
class GamePeriodAdmin(admin.ModelAdmin):
    readonly_fields = ('earliest_game_start', 'latest_game_start', )
    inlines = (GameInline, )
    list_display = ('label', 'season','get_league','get_sport', 'number', 'start_date', 'end_date', 'num_games', )
    read_write_fields = ['season', ]
    ordering = ['-start_date', 'number']

    fieldsets = (
        (None, {
            'fields': (
                'number',
                'season',
                ('earliest_game_start', 'latest_game_start', ),
            )
        }),
        (_('Advanced'), {
            'classes': ('collapse', ),
            'fields': (
                'period_id',
            )
        })
    )

    def get_queryset(self, request):
        qs = super(GamePeriodAdmin, self).get_queryset(request)
        return qs.annotate(num_games=Count('games'))

    def num_games(self, obj=None):
        return obj.num_games
    num_games.short_description = '# games'
    num_games.admin_order_field = 'num_games'

    def get_league(self, obj):
        return obj.season.league

    get_league.admin_order_field = 'num_teams'
    get_league.short_description = 'League'

    def get_sport(self, obj):
        return obj.season.league.sport

    get_sport.admin_order_field = 'get_sport'
    get_sport.short_description = 'Sport'

admin.site.register(GamePeriod, GamePeriodAdmin)


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('label', 'get_sport', 'league', 'name', 'type', 'start_date', 'end_date', 'hash' )
    readonly_fields = ('name', 'type', )
    inlines = (GamePeriodInline, )

    def get_sport(self, obj):
        return obj.league.sport

    get_sport.admin_order_field = 'get_sport'
    get_sport.short_description = 'Sport'

admin.site.register(Season, SeasonAdmin)


class TeamAdmin(LinkedFieldsMixin, ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'market', 'conference', 'division', 'venue', )
    list_filter = ('conference', )
    search_fields = ('name', 'market')
    inlines = (HomeGameInline, AwayGameInline, PlayersInline,  )
    fieldsets = (
        (None, {
            'fields': (
                'name', 'alias', 'market', 'conference', 'division', 'venue',
            )
        }),
        (_('Advanced'), {
            'classes': ('collapse', ),
            'fields': (
                'team_id',
            )
        })
    )

admin.site.register(Team, TeamAdmin)

class PlayerAdmin(LinkedFieldsMixin, ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('last_name', 'first_name',  'team','jersey_number','primary_position')
    list_filter = ('team',)

    fieldsets = (
        (None, {
            'fields': (
                'last_name', 'first_name', 'team','jersey_number','height','weight','position','primary_position','birth_date',
            )
        }),
        (_('Advanced'), {
            'classes': ('collapse',),
            'fields': (
                'player_id',
            )
        })
    )

admin.site.register(Player, PlayerAdmin)


class VenueAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'state', 'zip_code', )
    inlines = (TeamInline, GameInline, )
    fieldsets = (
        (None, {
            'fields': (
                'name', 'country', ('address', 'city', 'state', 'zip_code', ),
            )
        }),
        (_('Advanced'), {
            'classes': ('collapse', ),
            'fields': (
                'venue_id',
            )
        })
    )

admin.site.register(Venue, VenueAdmin)
