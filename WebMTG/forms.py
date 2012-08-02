from django import forms

class SearchForm(forms.Form):
    s = forms.CharField(max_length=30)