from django import forms
from .models import Csv


class CsvModelForm(forms.ModelForm):
    file_name = forms.FileField(label='')
    file_name.widget.attrs.update({'class': 'drop-zone__input'})
    class Meta:
        model = Csv
        fields = ('file_name',)

