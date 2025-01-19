from django.shortcuts import render, redirect
from ApplyPage.models import Resume
from .forms import LoginForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if user exists and password matches
            try:
                user = Resume.objects.get(email=username, password=password)
                messages.success(request, "Login successful!")
                return JsonResponse({
                    "message": "Login successful!",
                    "name": user.name,  # Assuming 'name' is a field in the 'Resume' model
                    "redirect": "/home"
                }, status=200)
                # Return a JSON response for a successful login
                #return JsonResponse({"message": "Login successful!", "redirect": "/home"}, status=200)
            except Resume.DoesNotExist:
                messages.error(request, "Invalid username or password.")
                return JsonResponse({"error": "Invalid username or password."}, status=400)
        else:
            return JsonResponse({"error": "Invalid form data."}, status=400)
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})
