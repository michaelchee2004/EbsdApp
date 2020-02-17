from django import forms
from .models import *

class CapitalForm(forms.ModelForm):
    class Meta:
        model = Capital
        fields = '__all__'


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = '__all__'
