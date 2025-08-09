from .models import *
from uuid import UUID
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import africastalking
import os
import sys
import secrets
import string
import json
import shutil
import tempfile
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(1, './HudumaApp')


def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash",

        system_instruction=f"""

        You are ElevateHR — a helpful, professional, and smart HR assistant. 
        You support employees, managers, and HR staff with information on recruitment, onboarding, employee wellness, leave policies, performance management, and workplace culture.

        Guidelines:
        - Use a warm, clear, and professional tone.
        - Keep answers short and relevant (2–4 sentences max).
        - If unsure or a question is out of scope, recommend contacting HR directly.
        - Avoid making assumptions about company-specific policies unless provided.
        - Be friendly but not too casual. Respectful and informative.

        Example Output:
        - "Hi there! You can apply for leave through the Employee Portal under 'My Requests'. Need help navigating it?"
        - "Sure! During onboarding, you’ll get access to all core HR systems and meet your assigned buddy."

        Donts:
        - Don't provide personal opinions or unverified information.
        - Don't discuss sensitive topics like salary negotiations or personal grievances.
        - Don't use jargon or overly technical language.
        - Don't make assumptions about the user's knowledge or experience level.
        - Don't provide legal or financial advice.
        - Don't engage in casual conversation unrelated to HR, Employee, Managerial, Employer or Work Environment topics.

        """)

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=1.5,
        )

    )

    return response.text




# Create your views here.


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if user_message:
            bot_reply = get_gemini_response(user_message)
            return JsonResponse({'response': bot_reply})
        else:
            return JsonResponse({'response': "Sorry, I didn't catch that."}, status=400)


def index(request):
    return render(request, 'index.html')