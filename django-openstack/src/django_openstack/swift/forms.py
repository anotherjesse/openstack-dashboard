# vim: tabstop=4 shiftwidth=4 softtabstop=4

"""
Forms used by various Swift views.
"""

import re

from django import forms

class CreateContainerForm(forms.Form):
    name = forms.CharField(max_length=256)

class UploadObjectForm(forms.Form):
    name = forms.CharField(max_length=256)
    object_file = forms.FileField()
