# vim: tabstop=4 shiftwidth=4 softtabstop=4

# TODO: license info

from django_openstack.swift.manager import SwiftManager


def get_project_or_404(request, project_id):
    """
    Again, this needs to be replaced with Keystone code.
    """
    return get_projects("notneeded")[0]

def get_projects(user):
    """
    Eventually this is where tenant info from Keystone will
    be retrieved.
    """
    class Project:
        pass
    placeholder = Project()
    placeholder.projectname = "tester"
    placeholder.description = "tester"
    return [placeholder]

def get_containers():
    """
    Returns a list of containers.
    """
    swift = SwiftManager()
    return swift.get_container_names()
