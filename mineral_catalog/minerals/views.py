from collections import OrderedDict
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import get_object_or_404, render


from .models import Mineral


def mineral_list(request):
    minerals = Mineral.objects.order_by(Lower('name'))
    return render(request, 'minerals/index.html', {'minerals': minerals})


def mineral_detail(request, pk):
    ordered_properties = OrderedDict()
    order = [
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
    return render(request, 'minerals/detail.html',
                  {'mineral': mineral, 'properties': ordered_properties})


def mineral_startswith(request, first_letter):
    minerals = Mineral.objects.filter(name__startswith=first_letter)
    return render(request, 'minerals/index.html', {'minerals': minerals})


def search(request):
    """Searches all the info displayed on the mineral detail page."""
    term = request.GET.get('q')
    minerals = Mineral.objects.filter(
        Q(name__icontains=term) |
        Q(image_caption__icontains=term) |
        Q(category__icontains=term) |
        Q(formula__icontains=term) |
        Q(strunz_classification__icontains=term) |
        Q(crystal_system__icontains=term) |
        Q(unit_cell__icontains=term) |
        Q(color__icontains=term) |
        Q(crystal_symmetry__icontains=term) |
        Q(cleavage__icontains=term) |
        Q(mohs_scale_hardness__icontains=term) |
        Q(luster__icontains=term) |
        Q(streak__icontains=term) |
        Q(diaphaneity__icontains=term) |
        Q(optical_properties__icontains=term) |
        Q(refractive_index__icontains=term) |
        Q(crystal_habit__icontains=term) |
        Q(specific_gravity__icontains=term)
    )
    return render(request, 'minerals/index.html', {'minerals': minerals})


def mineral_by_category(request, category):
    if category == 'other':
        minerals = Mineral.objects.exclude(
            Q(category__icontains='silicate') |
            Q(category__icontains='oxide') |
            Q(category__icontains='sulfate') |
            Q(category__icontains='sulfide') |
            Q(category__icontains='carbonate') |
            Q(category__icontains='halide') |
            Q(category__icontains='sulfosalt') |
            Q(category__icontains='phosphate') |
            Q(category__icontains='borate') |
            Q(category__icontains='organic') |
            Q(category__icontains='arsenate') |
            Q(category__icontains='native')
        )
    else:
        minerals = Mineral.objects.filter(category__icontains=category)
    return render(request, 'minerals/index.html', {'minerals': minerals})
