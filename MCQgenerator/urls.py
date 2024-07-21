from django.urls import path
from MCQgenerator import views


app_name="MCQgenerator"

urlpatterns=[
    path("",views.index,name="MCQgenerator"),
]