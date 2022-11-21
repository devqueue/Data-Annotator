from django import forms

options= [
    ('1', 'Rule'),
    ('0', 'Not Rule'),

    ]
    
class CHOICES(forms.Form):
    NUMS = forms.CharField(widget=forms.RadioSelect(choices=options))