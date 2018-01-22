from django import forms
from .models import Course, Assignment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'year', 'shortcut')
        widgets = {
            'year': forms.NumberInput(attrs={
                'length': 4,
                'min': 2018,
                'max': 2050
            }),
            'shortcut': forms.TextInput(attrs={
                'size': 11
            }),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('course', 'name_en', 'name', 'description_en', 'description', 'starting', 'ending',
                  'folder', 'training', 'fake_testing', 'testing')
        widgets = {
            'name_en': forms.TextInput(attrs={
                'size': 50
            }),
            'name': forms.TextInput(attrs={
                'size': 50
            }),
            'description_en': forms.Textarea(attrs={
                'cols': 50,
                'rows': 10
            }),
            'description': forms.Textarea(attrs={
                'cols': 50,
                'rows': 10
            }),
            'starting': forms.DateTimeInput(),
            'ending': forms.DateTimeInput(),
        }
