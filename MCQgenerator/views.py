from django.shortcuts import render
from .forms import DiseaseNameForm
from .LLM_Model.mcq_generator import getting_form
import json

def index(request):
    quiz_data=None
    quiz_para=None
    if request.method=="POST":
        form=DiseaseNameForm(request.POST)
        if form.is_valid():
            diseaseName=form.cleaned_data['name']
            Numbers=form.cleaned_data['nos']
            quiz_dataframe=getting_form(diseaseName,Numbers)
            quiz_json = quiz_dataframe.loc[0, 'quiz'].split('### RESPONSE_JSON\n')[1]
            quiz_data = json.loads(quiz_json)
            quiz_para = quiz_dataframe.loc[0,'para']
            
    else:
        form=DiseaseNameForm()
    
    context={
        "form":form,
        "quiz_df":quiz_data,
        "quiz_para":quiz_para,
    }
    return render(request, 'MCQgenerator/app/index.html',context)