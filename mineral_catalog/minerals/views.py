import operator

from collections import OrderedDict
from functools import reduce
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import render


from .models import Mineral


def mineral_list(request):
    """Shows a sorted by name list of minerals all or filtered by the first
    letter, color or category."""
    chosen_letter = request.GET.get('first_letter')
    chosen_color = request.GET.get('color')
    chosen_category = request.GET.get('category')

    minerals = Mineral.objects.order_by(Lower('name'))

    if chosen_letter:
        minerals = minerals.filter(name__startswith=chosen_letter)

    if chosen_color:
        if chosen_color == 'other':
            terms = [
                'red',
                'orange',
                'yellow',
                'green',
                'blue',
                'purple',
                'black',
                'white',
            ]

            query = reduce(operator.or_,
                           (Q(color__icontains=term) for term in terms))
            minerals = minerals.exclude(query)
        else:
            minerals = minerals.filter(color__icontains=chosen_color)
    else:
        chosen_color = 'all'

    if chosen_category:
        if chosen_category == 'other':
            terms = [
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
            ]

            query = reduce(operator.or_,
                           (Q(category__icontains=term) for term in terms))
            minerals = minerals.exclude(query)
        else:
            minerals = minerals.filter(category__icontains=chosen_category)
    else:
        chosen_category = 'all'

    return render(request, 'minerals/index.html', {
        'minerals': minerals,
        'chosen_letter': chosen_letter,
        'chosen_color': chosen_color,
        'chosen_category': chosen_category
    })


def mineral_detail(request, pk):
    """Shows mineral details."""
    ordered_properties = OrderedDict()
    order = [
        'name',
        'image_filename',
        'image_caption',
        'category',
        'formula',
        'color',
        'crystal_symmetry',
        'crystal_system',
        'unit_cell',
        'strunz_classification',
        'cleavage',
        'luster',
        'mohs_scale_hardness',
        'diaphaneity',
        'streak',
        'optical_properties'
    ]
    if Mineral.objects.filter(id=pk).exists():
        # Get a dictionary with all mineral fields.
        mineral = Mineral.objects.filter(id=pk).values()[0]
    else:
        raise Http404

    # Make an ordered dictionary with a predefined order.
    for key in order:
        # Add only those fields that have a value.
        if mineral[key]:
            ordered_properties[key] = mineral[key]

    # Get ids of alphabetically previous and next minerals.
    sorted_ids = Mineral.objects.order_by(Lower('name')).values_list('id',
                                                                     flat=True)
    sorted_ids = list(sorted_ids)
    current_id = sorted_ids.index(int(pk))

    # If the current mineral is the last in the list
    if int(pk) == sorted_ids[-1]:
        # Assign the first mineral in the list as the next.
        next_id = sorted_ids[0]
    else:
        next_id = sorted_ids[current_id+1]

    # If the current mineral is the first in the list
    if int(pk) == sorted_ids[0]:
        # Assign the last mineral in the list as the previous.
        previous_id = sorted_ids[-1]
    else:
        previous_id = sorted_ids[current_id-1]

    return render(request, 'minerals/detail.html', {
        'properties': ordered_properties,
        'next_id': next_id,
        'previous_id': previous_id,
    })


def search(request):
    """Searches all the info displayed on the mineral detail page."""
    term = request.GET.get('q')

    fields = [field.name for field in Mineral._meta.fields if field.name
              not in ['id', 'image_filename']]
    orm_lookups = ["%s__icontains" % field for field in fields]
    or_queries = [Q(**{orm_lookup: term}) for orm_lookup in orm_lookups]

    query = reduce(operator.or_, or_queries)
    minerals = Mineral.objects.filter(query)

    return render(request, 'minerals/index.html', {
        'minerals': minerals,
        'chosen_color': 'all',
        'chosen_category': 'all',
    })
