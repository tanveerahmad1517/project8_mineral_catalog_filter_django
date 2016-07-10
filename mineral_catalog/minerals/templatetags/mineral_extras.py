import random
from django import template
from django.utils.html import mark_safe

from minerals.models import Mineral


register = template.Library()


@register.inclusion_tag('minerals/random_mineral.html')
def random_mineral():
    """Returns a random mineral."""
    all_ids = Mineral.objects.values_list('id', flat=True)
    rand_id = random.choice(all_ids)
    mineral = Mineral.objects.get(id=rand_id)
    return {'mineral': mineral}


@register.inclusion_tag('minerals/filter_colors_categories.html')
def filter_colors_categories(chosen_color, chosen_category):
    """Creates filter by color and category."""
    categories = [
        'all',
        'silicate',
        'oxide',
        'sulfate',
        'sulfide',
        'carbonate',
        'halide',
        'sulfosalt',
        'phosphate',
        'borate',
        'organic',
        'arsenate',
        'native',
        'other',
    ]

    colors = [
        'all',
        'red',
        'orange',
        'yellow',
        'green',
        'blue',
        'purple',
        'black',
        'white',
        'other'
    ]

    return {'categories': categories, 'chosen_category': chosen_category,
            'colors': colors, 'chosen_color': chosen_color}


@register.simple_tag
def make_url(color, category):
    """Makes GET query to search by color and category."""
    if color == 'all' and category == 'all':
        return ''
    elif color == 'all':
        return 'category={}'.format(category)
    elif category == 'all':
        return 'color={}'.format(color)
    else:
        return 'category={}&color={}'.format(category, color)


@register.filter('underscore_to_space')
def underscore_to_space(string):
    """Changes underscore to a space."""
    new_string = string.replace('_', ' ')
    return new_string


@register.filter('highlight')
def highlight(word):
    """Adds HTML span tag to highlight a particular word."""
    return mark_safe("<span class='highlight'>%s</span>" % word)
