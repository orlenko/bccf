from django import forms
from django.template.loader import render_to_string
import logging

from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput


log = logging.getLogger(__name__)


class SelectWithPopUp(forms.Select):
    model = None

    def __init__(self, model=None, attrs=None, choices=()):
        self.model = model
        super(SelectWithPopUp, self).__init__(attrs, choices)

    def render(self, name, *args, **kwargs):
        html = super(SelectWithPopUp, self).render(name, *args, **kwargs)
        if not self.model:
            self.model = name
        popupplus = render_to_string("includes/formpopup.html", {'field': name, 'model': self.model})
        return html + popupplus


class AdvancedFileInput(ClearableFileInput):

    def __init__(self, *args, **kwargs):

        self.url_length = kwargs.pop('url_length',30)
        self.preview = kwargs.pop('preview',True)
        self.image_width = kwargs.pop('image_width',200)
        super(AdvancedFileInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None,):

        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'

        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):

            template = self.template_with_initial
            if self.preview:
                substitutions['initial'] = (u'<a href="{0}">{1}</a><br>\
                <a href="{0}" target="_blank"><img src="{0}" width="{2}"></a><br>'.format
                    (escape(value.url),'...'+escape(force_unicode(value))[-self.url_length:],
                     self.image_width))
            else:
                substitutions['initial'] = (u'<a href="{0}">{1}</a>'.format
                    (escape(value.url),'...'+escape(force_unicode(value))[-self.url_length:]))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)