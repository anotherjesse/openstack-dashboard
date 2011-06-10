# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
URL patterns for managing Swift.
"""

from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$',
        'django_openstack.swift.views.projects.index',
        name='swift_index'),
    url(r'^(?P<project_id>[^/]+)/$',
        'django_openstack.swift.views.projects.detail',
        name='swift_project'),
    url(r'^(?P<project_id>[^/]+)/containers$',
        'django_openstack.swift.views.containers.index',
        name='swift_containers'),
)
