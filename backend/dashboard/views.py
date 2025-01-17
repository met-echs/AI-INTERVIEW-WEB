# views.py
from django.shortcuts import render, redirect
from django.contrib import messages  # Import the messages module
from .models import EvaluationCriteria
from .forms import EvaluationCriteriaForm

def manage_evaluation_criteria(request):
    # If the request is POST, handle form submission or delete action
    if request.method == 'POST':
        if 'add_criteria' in request.POST:
            # If the "Add Criteria" form is submitted, save the new entry
            form = EvaluationCriteriaForm(request.POST)
            if form.is_valid():
                form.save()
                # Add success message
                messages.success(request, 'New evaluation criteria added successfully!')
                return redirect('manage_evaluation_criteria')  # Redirect after saving
            else:
                # If the form is not valid, add an error message
                messages.error(request, 'Failed to add new evaluation criteria. Please check the form.')
        elif 'delete_all' in request.POST:
            # If the "Delete All" button is pressed, delete all records
            EvaluationCriteria.objects.all().delete()
            # Add success message
            messages.success(request, 'All evaluation criteria deleted successfully!')
            return redirect('manage_evaluation_criteria')  # Redirect after deletion
    else:
        # If the request is GET, just fetch the data and show the form
        form = EvaluationCriteriaForm()
    
    # Fetch all existing evaluation criteria
    evaluation_criteria = EvaluationCriteria.objects.all()

    # Return both the form and the evaluation criteria to the template
    return render(request, 'evaluation_criteria_manage.html', {
        'form': form,
        'evaluation_criteria': evaluation_criteria
    })
