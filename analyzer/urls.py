"""
URL configuration for analyzer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # main outer app
    path('',include('core.urls')),

    # apps urls

    # datascience urls
    path('whats/',include('whatsapp.urls')),

    # machine learning urls
    path('rock/',include('rockmine.urls')),
    path('diabetes/',include('diabetes.urls')),
    path('moviesystem/',include('moviesystem.urls')),

    # LLMs Model project urls
    path('MCQgenerator/',include('MCQgenerator.urls')),
    path('asktoaske/',include('asktoaske.urls')),
    path('soundtext/',include('sound_img_txt.urls')),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)