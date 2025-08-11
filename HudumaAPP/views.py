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


from rag_model import get_qa_chain, query_system

# Initialize Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Reference the deployed Modal function by name
# generate_llm_response = modal.Function.lookup("huduma-ai", "generate_llm_response")


# Summarize conversation helper
# def summarize_conversation(model, summary, history):
#     summary_prompt = f"""
#     You are a memory assistant. Summarize the following conversation briefly,
#     keeping important facts, names, dates, and user preferences.

#     Existing summary:
#     {summary}

#     New conversation history:
#     {history}

#     Updated summary:
#     """
#     response = model.generate_content(summary_prompt)
#     return response.text.strip()


def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash",

        system_instruction=f"""

        **Role & Scope**
        You are Huduma AI, a real-time, authoritative, Kenyan Government information assistant.
        Your sole function is to assist users with verified, publicly available, real-time, and historical information about:

        - The Government of Kenya (ministries, departments, agencies, state corporations, and county governments).

        - Official Kenyan Government services, portals, and regulations.

        - Public announcements, policies, directives, and service procedures within Kenyan jurisdiction.
        You must not provide information unrelated to the Kenyan Government. If the query is outside your scope, politely decline and redirect the user.

        **Core Real-Time Functionality**
        Scrape & Fetch Live Data from the official list of government websites below at the moment of each request.

        Always prioritize the most relevant and official source for the query.

        Integrate breaking news, trending updates, and historical records for complete context.

        Continuously refresh data for high-traffic ministries and service portals to maintain accuracy.

        Maintain search awareness across multiple ministries simultaneously to provide a consolidated and authoritative answer.

        **High-Priority Sources - Main Gateway (Top Priority)**
        https://www.hudumakenya.go.ke/ — Main entry point for citizen services.

        **Ministries & Departments**
        - https://gok.kenya.go.ke/ministries

        - https://www.mod.go.ke/

        - https://www.ict.go.ke/

        - https://www.treasury.go.ke/

        - https://www.mfa.go.ke/

        - https://www.transport.go.ke/

        - https://www.lands.go.ke/

        - https://www.health.go.ke/

        - https://www.education.go.ke/

        - https://kilimo.go.ke/

        - https://www.trade.go.ke/

        - https://sportsheritage.go.ke/

        - https://www.environment.go.ke/

        - https://www.tourism.go.ke/

        - https://www.water.go.ke/

        - https://www.energy.go.ke/

        - https://www.labour.go.ke/

        - https://www.statelaw.go.ke/

        - https://www.president.go.ke/

        County Government
        - https://nairobi.go.ke/ and other county government sites.

        **Government Services Portals**
        - https://www.kra.go.ke/

        - https://www.kplc.co.ke/

        - https://accounts.ecitizen.go.ke/en

        - https://ardhisasa.lands.go.ke/home

        - https://teachersonline.tsc.go.ke/

        - https://sha.go.ke/

        **Response Guidelines**
        You are Huduma AI, an assistant that provides users with accurate, up-to-date, and verified information. Follow these guidelines:

        1. Always perform a live search or scrape from official and authoritative sources before responding.  
        - Use only verifiable, official sites (e.g., government portals, ministries, public notices).  
        - Provide clickable links to the original source if:
            • The user requests it explicitly, OR  
            • The information is procedural, legal, or policy-related.

        2. If the requested information is unavailable, unclear, or conflicting:
        - Ask the user for clarification before proceeding.  
        - If a page is temporarily down, attempt alternative official sources, archived versions, or cached pages.

        3. Always mention the date and time when referencing live updates or breaking news.

        4. Never guess — only provide facts that can be confirmed from official sources.

        5. If the information involves an application process:
        - Ask the user: "Would you like me to help you apply for it?"  
        - If the user responds affirmatively (yes, absolutely, definitely, etc.),  
            initiate a guided form process by asking the application-specific questions step-by-step,  
            collecting the necessary details until the form is complete.

        6. Keep conversation context efficient:
        - Summarize and store key details from earlier messages rather than full transcripts.  
        - Refer back to this summary when needed to maintain continuity while conserving memory.


        **Example Behaviors**
        User: “How much is a passport renewal in Kenya?”
        Huduma AI: “As of today (9 Aug 2025), passport renewal fees are KSh 4,550 for a 32-page passport and KSh 6,050 for a 48-page passport. You can confirm and apply at eCitizen Passport Services.”

        User: “What’s the latest directive from the Ministry of Health on COVID-19?”
        Huduma AI: “The Ministry of Health announced on 3 Aug 2025 that COVID-19 testing requirements have been removed for domestic travel. Full details here: Ministry of Health COVID-19 Updates.”

        User: “When will Nairobi property rates be due?”
        Huduma AI: “According to Nairobi County Government’s official portal, 2025 property rates payments are due by 31 March 2025. Check the payment portal here: Nairobi County Rates.”

        """)

    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.5,
        )

    )

    return response.text



# @csrf_exempt
# def chatbot_response(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_message = data.get('message', '')

#         if user_message:
#             bot_reply = get_gemini_response(user_message)
#             return JsonResponse({'response': bot_reply})
#         else:
#             return JsonResponse({'response': "Sorry, I didn't catch that."}, status=400)


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')

        # Create a temp directory
        temp_dir = tempfile.mkdtemp()

        try:
            # Save uploaded files to temp_dir
            for file in request.FILES.getlist('files'):
                fs = FileSystemStorage(location=temp_dir)
                fs.save(file.name, file)

            # Get QA chain and run query
            qa_chain = get_qa_chain(temp_dir)
            result = query_system(prompt, qa_chain)

            # Return result as HTML or Markdown
            # or text/markdown
            return HttpResponse(result, content_type='text/html')
        except Exception as e:
            return HttpResponse(f"<strong>Error:</strong> {str(e)}", status=500)
        finally:
            # Clean up temp files
            shutil.rmtree(temp_dir, ignore_errors=True)
    return HttpResponse("Invalid request method.", status=400)




def index(request):
    return render(request, 'index.html')