from django.urls import path
from asktoaske import views


app_name="asktoaske"

urlpatterns=[
    path("",views.index,name="asktoaske"),
    path("messages",views.messages,name="messages"),
    path('send-message/', views.send_message, name='send_message'),
]