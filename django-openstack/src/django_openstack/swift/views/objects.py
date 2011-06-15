# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Views for managing Swift objects.
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


LOG = logging.getLogger('django_openstack.swift')


@login_required
def index(request, project_id, container_id):
    project = shortcuts.get_project_or_404(request, project_id)

    manager = SwiftManager()
    objects = manager.get_container_storage_objects_info(container_id)

    return render_to_response('django_openstack/swift/objects/index.html', {
            'project': project,
            'container_name': container_id,
            'objects': objects,
            'upload_form': forms.UploadObjectForm()},
        context_instance=template.RequestContext(request))


@login_required
def upload(request, project_id, container_id):
    project = shortcuts.get_project_or_404(request, project_id)

    if request.method == 'POST':
        form = forms.UploadObjectForm(request.POST, request.FILES)
        
        manager = SwiftManager()
        if form.is_valid():
            object_name = form.cleaned_data['name']
            # the following is a terrible idea
            # need this to support chunking
            # also need some way to clean up files?
            manager.update_storage_object(
                container_id,
                object_name,
                request.FILES['object_file'].read())
            messages.success(request,
                             _('Object %s successfully uploaded.') % \
                             object_name)
            LOG.info('object "%s" successfully uploaded' %
                     object_name)
        else:
            objects = manager.get_container_storage_objects_info(container_id)
            return render_to_response(
                'django_openstack/swift/objects/index.html', {
                    'project': project,
                    'container_name': container_id,
                    'objects': objects,
                    'upload_form': form},
                context_instance=template.RequestContext(request))

    return redirect("swift_objects", project_id, container_id)


@login_required
def download(request, project_id, container_id, object_id):
    manager = SwiftManager()
    object_data = manager.get_storage_object_data(container_id, object_id)

    response = http.HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=%s' % object_id
    for data in object_data:
        response.write(data)
    return response


@login_required
def delete(request, project_id, container_id):
    object_name = request.POST['object_name']
    
    if request.method == 'POST':
        manager = SwiftManager()
        manager.delete_storage_object(container_id,
                                      object_name)
        LOG.info('object "%s" successfully deleted' % object_name)

    return redirect('swift_objects', project_id, container_id)
