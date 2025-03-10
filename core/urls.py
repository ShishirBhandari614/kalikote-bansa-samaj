from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('contact/', ContactMessageView.as_view(), name="contact"),

]