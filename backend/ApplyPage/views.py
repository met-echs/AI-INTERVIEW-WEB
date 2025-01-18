from django.shortcuts import render
from django.http import JsonResponse
import PyPDF2
from dashboard.models import EvaluationCriteria
from groq import Groq
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from datetime import datetime
from .models import Resume
client = Groq(api_key="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")


def generate_credentials(name):
    """Generate a random username and password."""
    first_name = name.split()[0].capitalize()
    current_year = datetime.now().year  # Get the current year
    password = f"{first_name}@{current_year}" 
    return password


def upload_resume(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        file = request.FILES.get('file')
        
        if name and email and file:
            try:
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'resumes'))
                filename = fs.save(file.name, file)
                file_path = os.path.join('resumes', filename)
                
                # Read the content of the uploaded PDF file
                pdf_reader = PyPDF2.PdfReader(file)
                file_content = ""
                
                # Extract text from each page of the PDF
                for page in pdf_reader.pages:
                    file_content += page.extract_text()
                
                # Clean up the extracted text (optional)
                file_content = file_content.strip()
                
                # Fetch the first evaluation criteria
                resume_criteria = EvaluationCriteria.objects.first()

                # Extract relevant fields from the evaluation criteria
                job_role = resume_criteria.job_role
                min_years_experience = resume_criteria.min_years_experience
                min_projects = resume_criteria.min_projects
                certifications_required = resume_criteria.certifications_required
                print(f"Name:{name}")
                print(f"Job Role: {job_role}")
                # print(f"Minimum Years Experience: {min_years_experience}")
                # print(f"Minimum Projects: {min_projects}")
                # print(f"Certifications Required: {certifications_required}")
                print
                # Define the resume text extracted from the file
                resume_text = file_content

                # Define the evaluation prompt
                prompt = f"""
                You are tasked with evaluating a resume based on the following criteria:

1. **Job Role**: Does the resume clearly specify a relevant job role for the position? The expected job role is: {job_role}.
2. **Work Experience**: Does the resume list at least {min_years_experience} years of relevant work experience related to the job role: {job_role}? Give extra 5 points if the experience is highly relevant.
3. **Number of Projects**: Does the resume list at least {min_projects} relevant projects related to the job role: {job_role}?
4. **Certifications**: Does the resume include relevant certifications? The expected certifications are: {certifications_required if certifications_required else "None"}.
5. **ATS Friendliness**: Is the resume formatted in a way that would be readable by an Applicant Tracking System (ATS)?

- Each of the four criteria (job role, work experience, number of projects, and certifications) will be rated from 0 to 25, and their total score will contribute to a final score out of 100.
- If any of the criteria are missing or poorly satisfied, reduce the score accordingly.
- If the job role criteria is not satisfied, set the overall score to 40.
- If the resume is **not ATS-friendly**, set the score to **-1**.

Return only the final score as a **number** between -1 and 100, without any explanation or breakdown.
                """

                # Request completion from the model
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",  # Use the best model for this task
                    messages=[{"role": "user", "content": prompt + resume_text}],
                    temperature=0.3,  # Use a lower temperature for consistent evaluation
                    max_completion_tokens=2024,
                    top_p=1,
                    stream=False,  # Set to False since we only need the final score
                )
                score = 0
                score = float(completion.choices[0].message.content.strip())
                print(f"Score:{score}")

                if score >= 50:
                    # Generate a random username and password
                    password = generate_credentials(name)
                    try:
                        Resume.objects.create(
                        name=name,
                        email=email,
                        password=password,
                        resume_score=score,
                        resume_link=file_path,
                        created_at=datetime.now()
                    )
                    except Exception as e:
                        return JsonResponse({"error": "Candidate already exists. Please check your email ID and try again."}, status=500)
                    return JsonResponse({"success": "Resume uploaded successfully."}, status=201)
                elif score < 50:
                    return JsonResponse({"error": "The resume did not meet the minimum criteria."}, status=400)
                elif score == -1:
                    return JsonResponse({"error": "The resume is not ATS-friendly."}, status=400)

            except Exception as e:
                return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
        else:
            return JsonResponse({"error": "All fields are required."}, status=400)

    # For GET request, render the form
    return render(request, "upload_form.html")
