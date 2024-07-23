from django.urls import path
from asktoaske import views


app_name="asktoaske"

urlpatterns=[
    path("",views.index,name="asktoaske"),
    path("ask/",views.asking,name="asking"),
    path("asking/",views.askingLLM,name="askingLLM"),
    path('send-message/', views.send_message, name='send_message'),
]