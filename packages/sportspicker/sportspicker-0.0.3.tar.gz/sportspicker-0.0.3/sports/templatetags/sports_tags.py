# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from num2words import num2words

from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

register = template.Library()


@register.filter
def ordinal_word(value):
    """Converts 1 => first, 2 => second, 3 => third."""
    try:
        value = int(value)
        return num2words(value, ordinal=True)
    except ValueError:
        return value
