 # vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Template tags for Swift projects.
"""

from django import template
from django_openstack.swift.shortcuts import get_projects


register = template.Library()


class ProjectsNode(template.Node):
    def render(self, context):
        # Store project list in template context.
        context['projects'] = get_projects(context['request'].user)
        return ''


@register.tag
def load_projects(parser, token):
    return ProjectsNode()
