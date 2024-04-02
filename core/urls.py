from django.urls import path
from core import views

app_name="core"

urlpatterns=[
    path("",views.index,name="index"),
    path("mr1/",views.path1,name="path1"),
    path("mr2/",views.path2,name="path2"),
    path("mr3/",views.path3,name="path3"),
    path("mr4/",views.path4,name="path4"),
    path("mr5/",views.path5,name="path5"),
    path("mr6/",views.path6,name="path6"),
    path("mr/",views.analysis,name="analysis"),
]