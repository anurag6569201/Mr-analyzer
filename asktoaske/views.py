from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import PDFDocumentForm
from .LLM_Model.test import get_response
import os
from django.conf import settings
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
            return redirect("asktoaske:messages")
    else:
        form = PDFDocumentForm()
    
    context = {
        'form': form
    }
    return render(request, 'asktoaske/app/index.html', context)

def messages(request):
    context = {

    }
    return render(request, 'asktoaske/app/messages.html',context)


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        if user_message:
            response_message = get_response(user_message)
            return JsonResponse({"reply": response_message})
        return JsonResponse({"reply": "I didn't understand that. Could you please rephrase?"})
    return JsonResponse({"error": "Invalid request method."}, status=405)