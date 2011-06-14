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
    url(r'^(?P<project_id>[^/]+)/containers/add$',
        'django_openstack.swift.views.containers.create',
        name='swift_container_create'),
    url(r'^(?P<project_id>[^/]+)/containers/delete$',
        'django_openstack.swift.views.containers.delete',
        name='swift_container_delete'),
    url(r'^(?P<project_id>[^/]+)/containers/(?P<container_id>[^/]+)$',
        'django_openstack.swift.views.objects.index',
        name='swift_objects'),
    url(r'^(?P<project_id>[^/]+)/containers/(?P<container_id>[^/]+)/upload$',
        'django_openstack.swift.views.objects.upload',
        name='swift_object_upload'),
    url(r'^(?P<project_id>[^/]+)/containers/(?P<container_id>[^/]+)/object/(?P<object_id>[^/]+)/download$',
        'django_openstack.swift.views.objects.download',
        name='swift_download_object'),
    url(r'^(?P<project_id>[^/]+)/containers/(?P<container_id>[^/]+)/objects/delete$',
        'django_openstack.swift.views.objects.delete',
        name='swift_object_delete'),
)
