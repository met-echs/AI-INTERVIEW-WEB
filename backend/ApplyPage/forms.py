from django import forms

class ResumeUploadForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
        label="Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        label="Email"
    )
    file = forms.FileField(
        label="Resume (PDF)",
        help_text="Upload your resume in PDF format."
    )
