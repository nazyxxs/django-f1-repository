# створення форми редагування Principal
from django import forms
from f1.models import Principals

class PrincipalForm(forms.ModelForm):
    class Meta:
        model = Principals
        fields = [
            'first_name',
            'last_name',
            'nationality',
            'birth_date',
            'team',          # ForeignKey
            'start_year',
            'end_year'
        ]
