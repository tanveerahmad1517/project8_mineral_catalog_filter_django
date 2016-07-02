from collections import OrderedDict
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, render


from .models import Mineral


def mineral_list(request):
    minerals = Mineral.objects.order_by(Lower('name'))
    return render(request, 'minerals/index.html', {'minerals': minerals})


def mineral_detail(request, pk):
    mineral_fields = {}
    ordered_mineral_properties = OrderedDict()
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
    mineral = get_object_or_404(Mineral, pk=pk)
    fields = mineral._meta.get_fields()
    # Make a dictionary with all mineral fields.
    for field in fields:
        mineral_fields[field.name] = getattr(mineral, field.name)
    # Make an ordered dictionary with a predefined order.
    for key in order:
        # Add only those fields that have a value.
        if mineral_fields[key]:
            ordered_mineral_properties[key] = mineral_fields[key]
    return render(request, 'minerals/detail.html',
                  {'mineral': mineral, 'fields': ordered_mineral_properties})


def mineral_startswith(request, first_letter):
    minerals = Mineral.objects.filter(name__startswith=first_letter)
    return render(request, 'minerals/index.html', {'minerals': minerals})


def search(request):
    term = request.GET.get('q')
    minerals = Mineral.objects.filter(
        Q(name__icontains=term)|
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