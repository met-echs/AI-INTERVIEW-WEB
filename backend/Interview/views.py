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
    return render(request, 'interview_start.html')

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
                # return JsonResponse({
                #     "message": "Login successful!",
                #     "name": user.name,  # Assuming 'name' is a field in the 'Resume' model
                # }, status=200)
                return render(request, 'interview_start.html', {'message': 'Resume uploaded and email sent successfully!'})
            except Resume.DoesNotExist:
                messages.error(request, "Invalid username or password.")
                return JsonResponse({"error": "Invalid username or password."}, status=400)
        else:
            return JsonResponse({"error": "Invalid form data."}, status=400)
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def get_question(request, question_id):
    try:
        # Try to get the question with the given ID
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        # If not found, fetch the next available question by ID
        question = Question.objects.order_by('id').first()
        if not question:
            # If no questions exist, return an error response
            return JsonResponse({"error": "No questions available."}, status=404)

    # Return the question text as JSON
    return JsonResponse({"question": question.question})

def evaluate_answer(question_text, response_text, specific_area, keywords):
    print("evaluate_answer")
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
    current_question_id = request.GET.get('question_id')
    print(" I AM STOPPING TRANSCRIPTION")
    if not current_question_id:
        return JsonResponse({"error": "Question ID not provided"}, status=400)
    
    try:
        # Try to get the question with the provided ID
        question = Question.objects.get(id=current_question_id)
    except Question.DoesNotExist:
        # If the question does not exist, try to fetch the next available question
        question = Question.objects.order_by('id').first()
        if not question:
            return JsonResponse({"error": "No questions available."}, status=404)

    score = evaluate_answer(
        question.question,       # The question text
        response_text_accumulator,  # The transcription or response text
        question.specific_area,  # The specific area
        question.keywords        # The comma-separated keywords
    )

    # Save response and score
    response = Response.objects.create(
        question=question,
        response_text=response_text_accumulator,
        score=score
    )

    response_data = {
        "question_id": current_question_id,
        "response": response_text_accumulator,
        "score": score,
        "status": "Recording stopped"
    }

    # Reset for the next question
    response_text_accumulator = ""
    current_question_id = None

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
