from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from archive.models import Dalal, District



class DalalFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All')] + list(Dalal.STATUS_CHOICES)

    search = forms.CharField(required=False, max_length=250, label='Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Dalal name'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    district = forms.ModelChoiceField(queryset=District.objects.all(), required=False,  widget=forms.Select(attrs={'class': 'form-select'}))
    