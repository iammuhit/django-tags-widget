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


class TagsInput(forms.JSONField):

    widget = TagsWidget

    def __init__(self, configs=None, **kwargs):
        self.configs = configs or {}
        self.configs_whitelist = self.whitelist(self.configs.get('options'))

        # Set widget with options
        if 'widget' not in kwargs:
            kwargs['widget'] = TagsWidget(configs=self.configs)
        elif isinstance(kwargs['widget'], type):
            kwargs['widget'] = kwargs['widget'](configs=self.configs)
        
        super().__init__(**kwargs)

    def to_python(self, value):
        """
        Convert the input value to a Python list of tags.
        Leverages JSONField's to_python for JSON parsing.
        
        Args:
            value: String (JSON) or list of tags
            
        Returns:
            List of tag dictionaries or strings
        """
        if not value or value == 'null':
            return []
        
        if isinstance(value, list):
            return value
        
        if isinstance(value, str):
            try:
                # Use parent's to_python for proper JSON parsing
                parsed = super().to_python(value)
                if parsed is None:
                    return []
                if isinstance(parsed, list):
                    return self._normalize_tags(parsed)
                return []
            except (ValidationError, ValueError, TypeError):
                # If not valid JSON, treat as comma-separated string
                return [tag.strip() for tag in value.split(',') if tag.strip()]
        
        return []
    
    def _normalize_tags(self, tags):
        """
        Convert tags from Tagify format to simple string list.
        Handles both [{"value": "tag"}] and ["tag"] formats.
        
        Args:
            tags: List of tags in various formats
            
        Returns:
            List of tag strings
        """
        normalized = []
        for tag in tags:
            if isinstance(tag, dict) and 'value' in tag:
                # Tagify format: {"value": "tag"}
                normalized.append(str(tag['value']))
            elif isinstance(tag, str):
                # Already a string
                normalized.append(tag)
            else:
                # Try to convert to string
                normalized.append(str(tag))
        return normalized
    
    def prepare_value(self, value):
        """
        Prepare value for rendering in the widget.
        Leverages JSONField's prepare_value for proper serialization.
        
        Args:
            value: List or JSON string of tags
            
        Returns:
            JSON string representation
        """
        if value is None or value == []:
            return ''
        
        if isinstance(value, str):
            try:
                # Validate it's proper JSON
                json.loads(value)
                return value
            except (json.JSONDecodeError, TypeError, ValueError):
                pass
        
        if isinstance(value, list):
            # Use parent's prepare_value for consistent JSON serialization
            return super().prepare_value(value)
        
        return super().prepare_value(value)
    
    def validate(self, value):
        """
        Validate the tag list.
        
        Args:
            value: List of tags
        """
        super().validate(value)
    
    def has_changed(self, initial, data):
        """
        Check if the field value has changed.
        Properly compares lists/JSON data.
        """
        if initial is None:
            initial = []
        if data is None:
            data = []
        return super().has_changed(initial, data)
    
    @classmethod
    def whitelist(cls, options):
        return options if isinstance(options, (list, tuple)) else ()
    