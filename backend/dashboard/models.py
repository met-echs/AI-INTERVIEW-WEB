# models.py
from django.db import models

class EvaluationCriteria(models.Model):
    job_role = models.CharField(max_length=255)
    min_years_experience = models.IntegerField(default=0)
    min_projects = models.IntegerField(default=0)
    certifications_required = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.job_role

class Question(models.Model):
    question_number = models.IntegerField(unique=True)
    question = models.TextField()
    specific_area = models.CharField(max_length=255)
    keywords = models.TextField(help_text="Comma-separated keywords")
    
    def __str__(self):
        return self.question_text
