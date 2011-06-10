# vim: tabstop=4 shiftwidth=4 softtabstop=4

# TODO: license info

from django_openstack.swift.manager import SwiftManager


def get_project_or_404(request, project_id):
    """
    Returns a project or 404s if it doesn't exist.
    """
    return get_projects()[0]

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
        Returns a list of containers associated with this user
        TODO: make this not hard coded for test account
       """
    #import pdb;pdb.set_trace()

    swift = SwiftManager('test', 'tester', 'testing')
    return swift.get_container_names()

