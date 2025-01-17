from django.shortcuts import render
from django.http import JsonResponse
import PyPDF2

def upload_resume(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        file = request.FILES.get('file')
        
        if name and email and file:
            try:
                # Read the content of the uploaded PDF file
                pdf_reader = PyPDF2.PdfReader(file)
                file_content = ""
                
                # Extract text from each page of the PDF
                for page in pdf_reader.pages:
                    file_content += page.extract_text()
                
                # Clean up the extracted text (optional)
                file_content = file_content.strip()

                # For now, print the data to the console
                # print(f"Name: {name}")
                # print(f"Email: {email}")
                # print(f"File Content:\n{file_content}")
                
            
            except Exception as e:
                return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
        else:
            return JsonResponse({"error": "All fields are required."}, status=400)
    
    # For GET request, render the form
    return render(request, "upload_form.html")
