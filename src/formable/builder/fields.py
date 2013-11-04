from django import forms
from django.forms.fields import Field
from django.utils import html
from django.forms.widgets import Widget

class StaticTextField(Field):
    """
    Custom field for Static Text and Static Seciton. Default widget is StaticText.
    """
    def __init__(self, value=None, *args, **kwargs):
        self.value = value
        super(StaticTextField, self).__init__(*args, **kwargs)
    
    def to_python(self, value=None):
        """
        Returns a unicode object
        """
        return smart_text(value)
        
    def widget_attrs(self, widget):
        return super(StaticTextField, self).widget_attrs(widget)

class StaticText(Widget):
    """
    Custom widget for the Static Text
    """
    value = None
    def __init__(self, value, attrs={}):
        self.value = value
        super(StaticText, self).__init__(attrs)
        
    def render(self, name, value, attrs=None):
        if self.value is None:
            self.value = "Static Text"
        return html.mark_safe(u'<span>%s</span>' % self.value)
        
        
class StaticSection(Widget):
    """
    Custom widget for the Static Section
    """
    value = None
    def __init__(self, value=None, attrs={}):
        self.value = value
        super(StaticSection, self).__init__(attrs)
        
    def render(self, name, value=None, attrs=None):
        if self.value is None:
            self.value = "Static Text"
        return html.mark_safe(u'<span class="section_head h3">%s</span>' % self.value)
        
