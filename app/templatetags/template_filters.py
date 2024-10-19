from enum import Flag
from django.template.defaulttags import register


@register.filter
def in_flag(needle: Flag, flag: Flag):
    return needle in flag
