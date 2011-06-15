# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Views for managing Swift.
"""

from django import http
from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django_openstack import log as logging
from django_openstack.swift import shortcuts


LOG = logging.getLogger('django_openstack.swift')


@login_required
def index(request):
    return render_to_response('django_openstack/swift/index.html', {
            'projects': shortcuts.get_projects(user=request.user)},
        context_instance=template.RequestContext(request))


@login_required
def detail(request, project_id):
    project = shortcuts.get_project_or_404(request, project_id)

    return render_to_response('django_openstack/swift/projects/index.html', {
            'project': project},
        context_instance=template.RequestContext(request))
