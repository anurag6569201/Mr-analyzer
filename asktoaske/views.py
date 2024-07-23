from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .forms import PDFDocumentForm
from analyzer.asktoaske_utils import getting_chunks_pdf
from .LLM_Model.conversation import creating_chroma_db
from .LLM_Model.conversation import getting_chroma_db

# from .LLM_Model.conversation import getting_pdf

def index(request):
    form_display=1
    loading=0
    messages=0
    if request.method == 'POST':
        form = PDFDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("asktoaske:asking")

    else:
        form = PDFDocumentForm()
    
    context = {
        'form_display':form_display,
        'loading':loading,
        'messages':messages,
        'form': form
    }
    return render(request, 'asktoaske/app/index.html',context)

def asking(request):
    form_display=0
    loading=1
    messages=0

    text_chunks=getting_chunks_pdf()
    vectordb=creating_chroma_db(text_chunks)
    finalchain=getting_chroma_db(vectordb)

    if finalchain:
        form_display=0
        loading=0
        messages=1
        redirect_url = reverse("asktoaske:askingLLM")
        return redirect(f"{redirect_url}?form_display={form_display}&loading={loading}&messages={messages}")
    
    context={
        'form_display':form_display,
        'loading':loading,
        'messages':messages,
    }
    return render(request, 'asktoaske/app/index.html',context)

def askingLLM(request):
    form_display=0
    loading=0
    messages=1
    context={
        'form_display':form_display,
        'loading':loading,
        'messages':messages,
    }
    return render(request, 'asktoaske/app/indexfinal.html',context)

def send_message(request):
    pass