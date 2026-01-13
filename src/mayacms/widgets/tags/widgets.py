import json

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TagsWidget(forms.TextInput):
    
    template_name = 'mayacms/forms/widgets/tags.html'

    class Media:
        css = {'all': ['forms/css/vendor/tagify.min.css']}
        js  = ['forms/js/vendor/tagify.min.js', 'forms/js/tags-widget.js']

    def __init__(self, attrs = None, configs=None):
        self.configs = configs or {}
        self.configs_whitelist = self.whitelist(self.configs.get('options'))
        default_attrs = {
            'data-max'     : False,
            'data-options': [],
            'data-provides': 'mayacms.forms.widgets.tags',
        }
        
        if attrs:
            default_attrs.update(attrs)
        
        if isinstance(configs, dict):
            default_attrs.update({
                'data-max'    : configs.get('max') or False,
                'data-enforce': configs.get('enforce') or False,
                'data-options': json.dumps(self.configs_whitelist),
            })

        super().__init__(attrs=default_attrs)

    @classmethod
    def whitelist(cls, options):
        return options if isinstance(options, (list, tuple)) else ()
