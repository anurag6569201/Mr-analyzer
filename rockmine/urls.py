from django.urls import path
from rockmine import views

app_name="rockmine"

urlpatterns=[
    path("",views.rockmine,name="rockmine"),
]