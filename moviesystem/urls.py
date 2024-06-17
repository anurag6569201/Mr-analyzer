from django.urls import path
from moviesystem import views


app_name="moviesystem"

urlpatterns=[
    path("",views.index,name="moviesystem"),
    path("result",views.result,name="moviesystem_result"),
]