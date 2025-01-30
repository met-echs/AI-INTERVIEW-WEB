from django.shortcuts import render, redirect, get_object_or_404
from ApplyPage.models import Resume
from .forms import LoginForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from backend.settings import DEEPGRAM_API_KEY
from backend.settings import GROQ_API_KEY
from groq import Groq
import speech_recognition as sr
from dashboard.models import Question, Response  # Ensure the Response model is imported

client = Groq(api_key=GROQ_API_KEY)

recognizer = sr.Recognizer()
microphone = sr.Microphone()
is_transcribing = False
response_text_accumulator = ""
current_question_id = 0

def index(request):
    return render(request, 'interview/interview_start.html')

def interview_test(request):
    return render(request, 'interview/interview_test.html')
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = Resume.objects.get(email=username, password=password)
                messages.success(request, "Login successful!")
                return render(request, 'interview/interview_home.html', {
                    'name': user.name  # Pass the user's name to the template
                })
            except Resume.DoesNotExist:
                messages.error(request, "Invalid username or password.")
                return JsonResponse({"error": "Invalid username or password."}, status=400)
        else:
            return JsonResponse({"error": "Invalid form data."}, status=400)
    else:
        form = LoginForm()
    
    return render(request, 'interview/Login.html', {'form': form})

def evaluate_answer(question_text, response_text, specific_area, keywords):
    print("evaluate_answer")
    print(f"question:{question_text}")
    print(f"response:{response_text}")                                                      
    completion = client.chat.completions.create(
    model="gemma2-9b-it",
    messages=[{
    "role": "system",
    "content": """You are an interviewer tasked with evaluating a candidate's response to a question.
    The response is transcribed from voice and may contain minor inaccuracies. Your task is to assess the answer based on the following:

    **Scoring Rules:**
    1. If the answer is completely empty, irrelevant, or nonsensical, assign a score of 0.
    2. If the answer is mostly incorrect, irrelevant, or poorly structured, assign a score between 1 and 5, with 1 being barely coherent and 5 being partially correct.
    3. If the answer is mostly correct, relevant, and coherent, assign a score between 6 and 10, with 10 being perfectly accurate, logical, and fully addressing the question.

    **Output Rules:**
    - Provide only a numerical score (0-10). 
    - Do not include any text, explanations, or additional comments."""
        }, 
        {
    "role": "user",
    "content": f"""Question: {question_text}
    Specific Area: {specific_area}
    Keywords: {keywords}
    Answer: {response_text}"""
        }],
        temperature=0.7,
        max_tokens=10,
        top_p=1,
        stream=False
    )
    score = completion.choices[0].message.content.strip()

    try:
        score = int(score)
        score = max(0, min(10, score))  # Ensure score is between 0 and 10
    except ValueError:
        score = 0  # Default to 0 if the score is not valid

    print(f"Score: {score}")
    return score



def get_question(request):
    question_number = request.GET.get('question_number')

    if question_number:
        try:
            question_number = int(question_number)
            question = Question.objects.get(question_number=question_number)
        except (Question.DoesNotExist, ValueError):
            return JsonResponse({
                "error": "Okay, the questions are finished. You can exit the interview.",
                "status": "finished"
            }, status=404)
    else:
        # Fetch the first question based on the smallest question_number
        question = Question.objects.order_by('question_number').first()
        if not question:
            return JsonResponse({
                "error": "Okay, the questions are finished. You can exit the interview.",
                "status": "finished"
            }, status=404)

    return JsonResponse({
        "question_number": question.question_number,
        "question_text": question.question,
        "status": "ok"
    })


def start_transcription(request):
    global is_transcribing
    global response_text_accumulator
    is_transcribing = True
    response_text_accumulator = ""
    response_data = {"status": "Recording started"}
    print(" I AM STARTING TRANSCRIPTION")
    return JsonResponse(response_data)

def stop_transcription(request):
    global is_transcribing, response_text_accumulator
    is_transcribing = False

    current_question_number = request.GET.get('question_number')

    if not current_question_number:
        return JsonResponse({"error": "Question number not provided"}, status=400)

    try:
        current_question_number = int(current_question_number)  # Convert to integer
        question = Question.objects.get(question_number=current_question_number)
    except (Question.DoesNotExist, ValueError):
        return JsonResponse({"error": "Invalid question number."}, status=404)

    # Evaluate the answer
    score = evaluate_answer(
        question.question,       
        response_text_accumulator,  
        question.specific_area,  
        question.keywords        
    )

    # Save response
    Response.objects.create(
        question=question,
        response_text=response_text_accumulator,
        score=score
    )

    # Fetch the next available question based on question_number order
    next_question = Question.objects.filter(question_number__gt=current_question_number).order_by('question_number').first()
    # print(f"Current question number: {current_question_number}")  # Debugging
    # print(f"Next question: {next_question.question}")  # Debugging

    if next_question:
        next_question_number = next_question.question_number
        next_question_text = next_question.question
    else:
        next_question_number = None
        next_question_text = "No more questions."
    # print(next_question_text)
    response_data = {
        "next_question_number": next_question_number,
        "next_question_text": next_question_text
    }

    # Reset response for next question
    response_text_accumulator = ""

    return JsonResponse(response_data)


def live_transcribe(request):
    global is_transcribing, response_text_accumulator
    print(" I AM LIVE TRANSCRIBING")
    if is_transcribing:
        try:
            with microphone as source:
                print("Listening...")
                audio = recognizer.listen(source)
                print("Processing audio...")
            try:
                text = recognizer.recognize_google(audio)
                print(f"Transcription: {text}")
                response_text_accumulator += " " + text
                return JsonResponse({"transcription": text})
            except sr.UnknownValueError:
                return JsonResponse({"error": "Could not understand audio"})
            except sr.RequestError as e:
                return JsonResponse({"error": f"Could not request results; {e}"})
        except OSError as e:
            return JsonResponse({"error": f"Microphone error: {e}"})
    else:
        return JsonResponse({"error": "Transcription is not active"})
