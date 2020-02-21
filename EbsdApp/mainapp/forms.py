from django import forms
from .models import *

class OptionForm(forms.Form):
    options = forms.ModelChoiceField(queryset=Option.objects.all())

