from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from mayacms.widgets.tags.widgets import TagsInput


class TagsField(models.JSONField):

    description = _('Tags')
    help_text   = _('Type and press Enter ...')
    data_attrs  = None
    
    def __init__(self, *args, configs=None, **kwargs):
        self.data_attrs = configs or {}

        # Ensure default is an empty list
        if 'default' not in kwargs:
            kwargs['default'] = list

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = TagsInput
        kwargs['configs'] = self.data_attrs
        return super().formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.data_attrs:
            kwargs['configs'] = self.data_attrs
        return (name, path, args, kwargs)
    
    def validate(self, value, model_instance):
        """
        Validate at the model level.
        """
        super().validate(value, model_instance)
        
    @classmethod
    def labels(cls):
        pass
