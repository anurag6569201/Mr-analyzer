from django.shortcuts import render,redirect
from .forms import FileUploadForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            contact_method = request.POST.get('contact_method')
            # print(contact_method)
            
            return redirect('core:analysis')
    else:
        form = FileUploadForm()
    return render(request,"core/index.html")

def analysis(request):
    return render(request,"core/analysis.html")