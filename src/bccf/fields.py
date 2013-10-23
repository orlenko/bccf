from django import forms
from bccf.widgets import AdvancedFileInput
from django.db.models.fields.files import ImageField
from south.modelsinspector import add_introspection_rules


class MyFormImageField(forms.ImageField):
    widget = AdvancedFileInput


class MyImageField(ImageField):
    def __init__(self, *args, **kwargs):
        for fb_arg in ("format", "extensions"):
            kwargs.pop(fb_arg, None)
        super(MyImageField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': MyFormImageField}
        defaults.update(kwargs)
        return super(MyImageField, self).formfield(**defaults)


add_introspection_rules([
    (
        [MyImageField],
        [],
        {},
    ),
], ['^bccf\.fields\.MyImageField'])

