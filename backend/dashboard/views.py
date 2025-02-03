# views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages  # Import the messages module
from .models import EvaluationCriteria
from .forms import EvaluationCriteriaForm
from .models import Question
from .forms import QuestionCriteriaForm


def manage_evaluation_criteria(request):
    if request.method == 'POST':
        if 'add_criteria' in request.POST:
            # Handle new criteria addition
            form = EvaluationCriteriaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'New evaluation criteria added successfully!')
                return redirect('manage_evaluation_criteria')
            else:
                messages.error(request, 'Failed to add new evaluation criteria. Please check the form.')

        elif 'update_criteria' in request.POST:
            # Handle updating existing criteria
            criteria_id = request.POST.get('criteria_id')
            criteria = get_object_or_404(EvaluationCriteria, id=criteria_id)
            form = EvaluationCriteriaForm(request.POST, instance=criteria)
            if form.is_valid():
                form.save()
                messages.success(request, 'Evaluation criteria updated successfully!')
                return redirect('manage_evaluation_criteria')
            else:
                messages.error(request, 'Failed to update criteria. Please check the form.')

    else:
        form = EvaluationCriteriaForm()

    evaluation_criteria = EvaluationCriteria.objects.all()
    return render(request, 'evaluation_criteria_manage.html', {
        'form': form,
        'evaluation_criteria': evaluation_criteria
    })

from django.http import JsonResponse

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
            
            
                
        elif 'edit_criteria' in request.POST:
            criteria_id = request.POST.get('criteria_id')
            criteria = get_object_or_404(Question, id=criteria_id)
            form = QuestionCriteriaForm(request.POST, instance=criteria)
            if form.is_valid():
                form.save()
                messages.success(request, 'Question criteria updated successfully!')
                return redirect('question_manage_criteria')
            else:
                messages.error(request, 'Failed to update question criteria. Please check the form.')

        elif 'delete_all' in request.POST:
            Question.objects.all().delete()
            messages.success(request, 'All question criteria deleted successfully!')
            return redirect('question_manage_criteria')

    else:
        form = QuestionCriteriaForm()

    criteria_list = Question.objects.all().order_by('question_number')

    return render(request, 'question_criteria_manage.html', {
        'form': form,
        'criteria_list': criteria_list
    })

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return redirect('question_manage_criteria')