from django import forms
from .models import Person


class PersonProfileForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'date_of_birth',
                  'country', 'city', 'experience', 'messenger', 'photo',]
