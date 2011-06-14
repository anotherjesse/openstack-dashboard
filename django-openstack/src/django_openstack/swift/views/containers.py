# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Views for managing Swift containers.
"""

from django import http
from django import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django_openstack import log as logging
from django_openstack.swift import forms
from django_openstack.swift import shortcuts
from django_openstack.swift.manager import SwiftManager


LOG = logging.getLogger('django_openstack.swift')


@login_required
def index(request, project_id):
    project = shortcuts.get_project_or_404(request, project_id)
    
    containers = shortcuts.get_containers()
    
    return render_to_response('django_openstack/swift/containers/index.html', {
        'project': project,
        'containers': containers,
        'create_form': forms.CreateContainerForm()
    }, context_instance=template.RequestContext(request))

@login_required
def create(request, project_id):
    project = shortcuts.get_project_or_404(request, project_id)
    
    if request.method == 'POST':
        form = forms.CreateContainerForm(request.POST)
        
        if form.is_valid():
            manager = SwiftManager()
            manager.create_container(form.cleaned_data['name'])
        else:
            containers = shortcuts.get_containers()

            return render_to_response('django_openstack/swift/containers/index.html', {
                'project': project,
                'containers': containers,
                'create_form': form
            }, context_instance=template.RequestContext(request))
            
    return redirect('swift_containers', project_id)

@login_required
def delete(request, project_id):
    if request.method == 'POST':
        manager = SwiftManager()
        manager.delete_container(request.POST['container_name'])

    return redirect('swift_containers', project_id)
