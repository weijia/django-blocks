from django import forms

class GlobalSearchForm(forms.Form):
    query = forms.CharField(max_length=100)
