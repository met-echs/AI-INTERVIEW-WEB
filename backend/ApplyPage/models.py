from django.db import models

# Create your models here.
class Resume(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    password = models.CharField(max_length=255, verbose_name="Password")
    resume_score = models.IntegerField(
        null=True, blank=True, 
        verbose_name="Resume Score", 
        help_text="Score for the resume (0-100)",
    )
    resume_link = models.URLField(verbose_name="Resume Link")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.name
