from django.urls import path
from .views import *
app_name = 'gallery'



urlpatterns = [
    path('list/', custom_form_list, name='custom_form_list'),
    path('detail/<int:pk>/', custom_form_detail, name='custom_form_detail'),
]



