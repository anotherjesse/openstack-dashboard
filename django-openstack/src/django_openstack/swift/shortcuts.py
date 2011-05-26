# vim: tabstop=4 shiftwidth=4 softtabstop=4

# TODO: license info

from django_openstack.swift.manager import SwiftManager



def get_containers():
    """
        Returns a list of containers associated with this user
        TODO: make this not hard coded for test account
       """
    #import pdb;pdb.set_trace()

    swift = SwiftManager('test', 'tester', 'testing')
    return swift.get_container_names()




