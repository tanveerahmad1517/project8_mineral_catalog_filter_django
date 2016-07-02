import random
from urllib.parse import quote
from django import template
from django.db.models import Count
from django.utils.six.moves.urllib.parse import unquote

from minerals.models import Mineral


register = template.Library()


@register.inclusion_tag('minerals/random_mineral.html')
def random_mineral():
    """Returns a random mineral."""
    total = Mineral.objects.count()
    rand_id = random.randint(1, total)
    mineral = Mineral.objects.get(id=rand_id)
    return {'mineral': mineral}


@register.filter('underscore_to_space')
def underscore_to_space(string):
    """Changes underscore to a space."""
    new_string = string.replace('_', ' ')
    return new_string


@register.filter('url_decode')
def url_decode(value):
    new_value = unquote(value)
    return new_value


@register.filter('url_quote')
def url_quote(value):
    new_value = quote(value)
    return new_value