from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)
from .forms import PDFDocumentForm
from .LLM_Model.test1 import get_response
import os
from django.conf import settings




# LLM model using hugging face
from .LLM_Model.test1 import initialize_chromadb
from analyzer.asktoaske_hugging import text_split

def index(request):
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            pdfs_path = os.path.join(settings.MEDIA_ROOT, 'pdfs/')
            for filename in os.listdir(pdfs_path):
                file_path = os.path.join(pdfs_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            form.save()
            text_chunks = text_split()
            initialize_chromadb(text_chunks)
            return redirect("asktoaske:messages")
    else:
        form = PDFDocumentForm()
    
    context = {
        'form': form
    }
    return render(request, 'asktoaske/app/index.html', context)

def messages(request):
    return render(request, 'asktoaske/app/messages.html')

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            if user_message:
                response_message = get_response(user_message)
                return JsonResponse({"reply": response_message})
            return JsonResponse({"reply": "I didn't understand that. Could you please rephrase?"})
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)