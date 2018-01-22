from django import forms
from .models import Course, Assignment, Submission


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'year')
        widgets = {
            'year': forms.NumberInput(attrs={
                'length': 4,
                'min': 2018,
                'max': 2050
            }),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('course', 'name_en', 'name', 'description_en', 'description', 'starting', 'ending',
                  'folder', 'training', 'fake_testing', 'testing', 'measurement', 'sorting', 'threshold')
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


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('submitted_file', )
        widgets = {
            'submitted_file': forms.FileInput(attrs={
                'accept': '.py'
            })
        }
