from django.urls import path
from asktoaske import views


app_name="asktoaske"

urlpatterns=[
    path("",views.index,name="asktoaske"),
]