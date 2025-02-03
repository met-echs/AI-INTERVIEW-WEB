# forms.py
from django import forms
from .models import EvaluationCriteria
from .models import Question

class EvaluationCriteriaForm(forms.ModelForm):
    class Meta:
        model = EvaluationCriteria
        fields = ['job_role', 'min_years_experience', 'min_projects', 'certifications_required']

class QuestionCriteriaForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_number', 'question', 'specific_area', 'keywords']  # Ensure these fields exist in the model
        widgets = {
            'question_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'specific_area': forms.TextInput(attrs={'class': 'form-control'}),
            'keywords': forms.TextInput(attrs={'class': 'form-control'}),
        }
