# views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages  # Import the messages module
from .models import EvaluationCriteria
from .forms import EvaluationCriteriaForm
from .models import Question
from .forms import QuestionCriteriaForm

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
def question_manage_criteria(request):
    if request.method == 'POST':
        if 'add_criteria' in request.POST:
            form = QuestionCriteriaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'New question criteria added successfully!')
                return redirect('question_manage_criteria')
            else:
                messages.error(request, 'Failed to add question criteria. Please check the form.')
        elif 'delete_criteria' in request.POST:
            criteria_id = request.POST.get('criteria_id')
            criteria = get_object_or_404(Question, id=criteria_id)
            criteria_number = criteria.question_number  # Capture the question number before deleting
            criteria.delete()
            messages.success(request, 'Question criteria deleted successfully!')

            # Find the next question based on the question_number
            next_question = Question.objects.filter(question_number__gt=criteria_number).order_by('question_number').first()
            if next_question:
                return redirect('question_detail', question_id=next_question.id)
            else:
                messages.info(request, 'No next question available.')
                return redirect('question_manage_criteria')
        elif 'delete_all' in request.POST:
            Question.objects.all().delete()
            messages.success(request, 'All question criteria deleted successfully!')
            return redirect('question_manage_criteria')
    else:
        form = QuestionCriteriaForm()

    # Get all questions ordered by question_number
    criteria_list = Question.objects.all().order_by('question_number')

    return render(request, 'question_criteria_manage.html', {
        'form': form,
        'criteria_list': criteria_list
    })
