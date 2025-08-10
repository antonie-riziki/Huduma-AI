from .models import *
from uuid import UUID
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
import africastalking
import modal
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

# Initialize Google Generative AI
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Reference the deployed Modal function by name
generate_llm_response = modal.Function.lookup("huduma-ai", "generate_llm_response")


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_prompt = data.get("prompt", "")

        # Call Modal function and wait for result
        ai_reply = generate_llm_response.remote(user_prompt).get()

        return JsonResponse({"response": ai_reply})

    return JsonResponse({"error": "Invalid request"}, status=400)



def index(request):
    return render(request, 'index.html')