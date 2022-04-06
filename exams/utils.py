import os
from django.core.exceptions import ValidationError
from django.db import models

class ExtFileField(models.FileField):
  """
  Same as models.FileField, but you can specify a file extension whitelist.
  """
  def __init__(self, *args, **kwargs):
    ext_whitelist = kwargs.pop("ext_whitelist")
    self.ext_whitelist = [i.lower() for i in ext_whitelist]

    super(ExtFileField, self).__init__(*args, **kwargs)

  def deconstruct(self):
    name, path, args, kwargs = super().deconstruct()
    kwargs['ext_whitelist'] = self.ext_whitelist
    return name, path, args, kwargs

  def clean(self, *args, **kwargs):
    data = super(ExtFileField, self).clean(*args, **kwargs)
    filename = data.name
    ext = os.path.splitext(filename)[1]
    ext = ext.lower()
    if ext not in self.ext_whitelist:
      raise ValidationError("Not allowed filetype!")
    return data
