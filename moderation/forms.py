from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from archive.models import Dalal, District


class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    
class DalalForm(forms.ModelForm):

    class Meta:
        model = Dalal

        exclude = ['date_added']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            model_field = self._meta.model._meta.get_field(field_name)

            if getattr(model_field, 'blank', False):
                if field.label and '(optional)' not in field.label.lower():
                    field.label = f"{field.label} (optional)"    

            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'



class DalalFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All')] + list(Dalal.STATUS_CHOICES)

    search = forms.CharField(required=False, max_length=250, label='Name')
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    district = forms.ModelChoiceField(queryset=District.objects.all(), required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
