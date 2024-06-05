from django.urls import path
from creditscore import views

app_name="creditscore"

urlpatterns=[
    path("",views.credit,name="credit"),
]