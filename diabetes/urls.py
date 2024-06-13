from django.urls import path
from diabetes import views

app_name="diabetes"

urlpatterns=[
    path("",views.index,name="diabetes"),
]