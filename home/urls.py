"""task1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from home import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.loginn,name='loginn'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logoutt,name='logoutt'),
    path('viewb',views.viewd,name='viewb'),
    path('blog',views.blog,name='blog'),
    path('dash',views.dash,name='dash'),
    path('viewp',views.viewp,name='viewp'),
    path('blog/<int:sno>',views.blogpost,name='blogpost'),
    path('viewdoc',views.viewdoc,name='viewdoc'),
    path('bookapp/<int:sno>',views.bookapp,name='bookapp'),
    path('chat/<room_code>',views.chat,name='chat'),
    # path('chatt',views.docchat,name='docchat'),
]+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)