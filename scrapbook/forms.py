from django import forms
from django.utils.safestring import SafeString


class BaseForm(forms.ModelForm):
    '''Base form class wrappers'''
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def as_div(self):
        return SafeString(super().as_div().replace("<div>", "<div class='form-group mb-3'>"))