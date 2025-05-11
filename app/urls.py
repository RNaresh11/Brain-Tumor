from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.base,name="base"),
    path("home/",views.home,name="home"),
    path("details/",views.details,name='details'),
    path("detect/",views.detect,name="detect"),
    
    path("login/",views.user_login,name="login"),
    path("register/",views.register,name='register'),
    path('logout/',views.user_logout,name='logout')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)