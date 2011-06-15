# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Views for managing Swift containers.
"""

from django import http
from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.utils.translation import ugettext as _
from django_openstack import log as logging
from django_openstack.swift import forms
from django_openstack.swift import shortcuts
from django_openstack.swift.manager import SwiftManager
from cloudfiles.errors import ContainerNotEmpty

LOG = logging.getLogger('django_openstack.swift')


@login_required
def index(request, project_id):
    project = shortcuts.get_project_or_404(request, project_id)

    containers = shortcuts.get_containers()

    return render_to_response('django_openstack/swift/containers/index.html', {
            'project': project,
            'containers': containers,
            'create_form': forms.CreateContainerForm()},
        context_instance=template.RequestContext(request))


@login_required
def create(request, project_id):
    project = shortcuts.get_project_or_404(request, project_id)

    if request.method == 'POST':
        form = forms.CreateContainerForm(request.POST)

        if form.is_valid():
            manager = SwiftManager()
            container_name = form.cleaned_data['name']
            manager.create_container(container_name)
            messages.success(request,
                             _('Container %s successfully created.') % \
                             container_name)
            LOG.info('Container "%s" successfully created' % container_name)
        else:
            containers = shortcuts.get_containers()

            return render_to_response(
                'django_openstack/swift/containers/index.html', {
                    'project': project,
                    'containers': containers,
                    'create_form': form},
                context_instance=template.RequestContext(request))

    return redirect('swift_containers', project_id)


@login_required
def delete(request, project_id):
    if request.method == 'POST':
        manager = SwiftManager()
        container_name = request.POST['container_name']

        try:
            manager.delete_container(container_name)
        except ContainerNotEmpty, e:
            messages.error(request,
                           _('Unable to delete non-empty container: %s') % \
                           container_name)
            LOG.error('Unable to delete container "%s".  Exception: "%s"' %
                      (container_name, str(e)))
        else:
            messages.success(request,
                             _('Container %s successfully deleted.') % \
                             container_name)
            LOG.info('Container "%s" successfully deleted' % container_name)

    return redirect('swift_containers', project_id)
