# forms.py
from django import forms
from .models import EvaluationCriteria

class EvaluationCriteriaForm(forms.ModelForm):
    class Meta:
        model = EvaluationCriteria
        fields = ['job_role', 'min_years_experience', 'min_projects', 'certifications_required']
