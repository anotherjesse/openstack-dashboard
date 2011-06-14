#!/usr/bin/env python
"""
Incredibly stupid layer sitting in front of python-cloudfiles.
Makes it so that the UI doesn't have to keep track of containers or
connections

"""

import cloudfiles
from django.conf import settings
from exceptions import ContainerAlreadyExistsError

class SwiftManager(object):
    def __init__(self):
        self.authuser = settings.SWIFT_ACCOUNT + ':' + settings.SWIFT_USER
        self.password = settings.SWIFT_PASS
        self.authurl = settings.SWIFT_AUTHURL
        
    def get_swift_connection(self):
        return cloudfiles.get_connection(self.authuser, self.password,
                                  authurl=self.authurl)

    def get_container_names(self):
        conn = self.get_swift_connection()
        containers = conn.get_all_containers()
        return [{"name":c.name} for c in containers]

    def get_container_storage_objects_info(self, container_name):
        conn = self.get_swift_connection()
        container = conn.get_container(container_name)
        container_objects = container.get_objects()
        return [{"name":o.name, "last_modified":o.last_modified} for o in
                container_objects]

    def get_storage_object_data(self, container_name, storage_object_name):
        """
        Returns a generator that produces the objects data
        """
        conn = self.get_swift_connection()
        container = conn.get_container(container_name)
        storage_object = container.get_object(storage_object_name)
        # No point in storing the file in memory unless that's the intention of
        # the caller
        return storage_object.stream()

    def create_container(self, container_name):
        """
        Creates a container. Throws a ContainerAlreadyExistsError if the
        Container already exists
        """
        # cloudfiles create_container() doesn't throw error on existing
        # container name
        conn = self.get_swift_connection()
        if container_name in self.get_container_names():
            raise ContainerAlreadyExistsError()

        conn.create_container(container_name)

    def delete_container(self, container_name):
        """
        Deletes container.  cloudfiles may throw NoSuchContainer or
        ContainerNotEmpty
        """
        conn = self.get_swift_connection()
        conn.delete_container(container_name)

    def delete_storage_object(self, container_name, storage_object_name):
        """
        Deletes object.  cloudfiles may throw NoSuchObject
        """
        conn = self.get_swift_connection()
        container = conn.get_container(container_name)
        container.delete_object(storage_object_name)

    def update_storage_object(self, container_name, storage_object_name,
                              storage_object_data):
        """
        Creates/Updates a storage object
        """
        conn = self.get_swift_connection()
        container = conn.get_container(container_name)
        # works properly if object already exists
        storage_object = container.create_object(storage_object_name)
        # supports progress callback
        storage_object.write(storage_object_data)
