# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Errors related to Swift's API
"""

class ContainerAlreadyExistsError(StandardError):
    """
    An attempt to create a container that already exists was made
    """
    pass

def wrap_swift_error(func):
    pass
