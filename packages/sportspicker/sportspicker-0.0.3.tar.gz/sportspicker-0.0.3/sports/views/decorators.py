# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def sports_admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Allows access to the decorated View if user `is_sportsadmin` or `is_staff`
    """
    actual_decorator = user_passes_test(
        lambda u: u.user_data.is_sportsadmin or u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
