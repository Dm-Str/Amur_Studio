from django import forms
from .models import Person, Lesson


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['content', 'home_work']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['home_work'].widget.attrs.update({'class': 'form-control'})


class PersonProfileForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'date_of_birth',
                  'city', 'experience', 'messenger', 'photo',]