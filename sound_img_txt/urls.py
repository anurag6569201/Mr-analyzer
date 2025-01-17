from django.urls import path
from sound_img_txt import views


app_name="sound_img_txt"

urlpatterns=[
    path("",views.index,name="index"),
]