from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect


def hello(request):
    return HttpResponseRedirect(reverse('minerals:list'))
