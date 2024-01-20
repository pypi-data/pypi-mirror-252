# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.generic import DetailView, ListView, UpdateView

from ..models import Conference, Game, Team

from .decorators import sports_admin_required
from .forms import GameForm


class SportAdminMixin(object):
    @method_decorator(sports_admin_required())
    def dispatch(self, request, *args, **kwargs):
        return super(SportAdminMixin, self).dispatch(request, *args, **kwargs)


class ConferenceMixin(object):
    @cached_property
    def conference(self):
        return Conference.objects.filter(pk=self.kwargs.get('conference_pk', -1)).first()

    def get_context_data(self, **kwargs):
        context = super(ConferenceMixin, self).get_context_data(**kwargs)
        context['conference'] = self.conference
        return context


class ConferenceListView(SportAdminMixin, ListView):
    model = Conference
    http_method_names = ['get', ]

    def get_queryset(self):
        qs = super(ConferenceListView, self).get_queryset()
        return qs.order_by('name')


class ConferenceDetailView(SportAdminMixin, DetailView):
    model = Conference
    pk_url_kwarg = 'conference_pk'


class TeamDetailView(SportAdminMixin, ConferenceMixin, DetailView):
    model = Team
    pk_url_kwarg = 'team_pk'

    def get_object(self, queryset=None):
        return super(TeamDetailView, self).get_object(queryset=queryset)

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        team = self.get_object()
        context['games'] = (Game.objects.filter(Q(home_id=team.pk) | Q(away_id=team.pk))
                                        .annotate(season=F('game_period__season__label'))
                                        .order_by('scheduled'))
        return context


class GameDetailView(SportAdminMixin, UpdateView):
    model = Game
    form_class = GameForm
    pk_url_kwarg = 'game_pk'
    template_name = 'sports/game_detail.html'
    # This will store the value of 'next', if provided
    redirect_url = None

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save()
        redirect_url = form.cleaned_data['redirect_url']
        return HttpResponseRedirect(redirect_url or self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(GameDetailView, self).get_form_kwargs()
        kwargs.update({'redirect_url': self.redirect_url})
        return kwargs

    def get(self, request, *args, **kwargs):
        """
        If a `next` is set, ensure its added to the form.
        """
        self.redirect_url = request.GET.get('next', None)
        return super(GameDetailView, self).get(request, *args, **kwargs)
