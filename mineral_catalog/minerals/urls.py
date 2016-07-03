from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.mineral_list, name='list'),
    url(r'(?P<pk>\d+)/$', views.mineral_detail, name='detail'),
    url(r'search/$', views.search, name='search'),
    url(r'category/(?P<category>[a-z]+)/$', views.mineral_by_category,
        name='category'),
    url(r'color/(?P<color>[a-z]+)/$', views.mineral_by_color, name='color'),
    url(r'name-begins/(?P<first_letter>[a-z])/$', views.mineral_startswith,
        name='startswith'),
]
urlpatterns += staticfiles_urlpatterns()
