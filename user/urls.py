
from . import views
from django.urls import path

urlpatterns = [
    path('register/',views.register),
    path('check_phone/',views.check_phone),
    path('verification/',views.ver_code),
]
