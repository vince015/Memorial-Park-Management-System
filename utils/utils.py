from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import resolve_url
from django.urls import reverse

def get_branches(user):
    group_names = ['Baliwag', 'San Rafael', 'San Miguel']

    user_groups = user.groups.filter(name__in=group_names)
    branches = []
    for user_group in user_groups:
        branches.append(user_group.branch)

    return branches
