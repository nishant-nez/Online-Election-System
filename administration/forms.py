from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from elections.models import Election, Candidate

class ElectionCreateForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'is_active']
        labels = {
            'is_acive': 'Active',
        }
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create Election'))


class ElectionUpdateForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'image', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CandidateCreateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Candidate
        fields = ['name', 'description', 'dob', 'gender', 'image', 'election']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

        def __init__(self, *args, **kwargs):
            super(CandidateCreateForm, self).__init__(*args, **kwargs)
            self.fields['election'].queryset = Election.objects.all()


class CandidateUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Candidate
        fields = ['name', 'description', 'dob', 'gender', 'image', 'election']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
