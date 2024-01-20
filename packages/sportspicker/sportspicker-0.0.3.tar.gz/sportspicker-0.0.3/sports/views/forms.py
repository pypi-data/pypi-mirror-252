# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms

from ..models import Game


class ReadOnlyFieldsMixin(object):
    # TODO: This should be updated when the project upgrades to Django 1.9+.
    # See: https://docs.djangoproject.com/en/1.9/ref/forms/fields/#disabled
    readonly_fields = []

    def __init__(self, *args, **kwargs):
        """
        Sets the widgets for the read-only fields to be readonly.
        """
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.readonly_fields:
                self.fields[field].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        """
        Ensures that no form-hacking had occurred for the read-only fields
        """
        cleaned_data = super(ReadOnlyFieldsMixin, self).clean()
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.readonly_fields:
                cleaned_data[field] = getattr(instance, field, None)
        return cleaned_data


class GameForm(ReadOnlyFieldsMixin, forms.ModelForm):
    readonly_fields = ['game_id', 'coverage', 'status', ]

    redirect_url = forms.CharField(max_length=4096, widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        redirect_url = kwargs.pop('redirect_url', None)
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['redirect_url'].initial = redirect_url

    class Meta:
        model = Game
        fields = [
            'redirect_url',
            'game_id',
            'game_period',
            'scheduled', 'coverage', 'status',
            'away',
            'home',
            'away_points',
            'home_points',
            'venue',
        ]
