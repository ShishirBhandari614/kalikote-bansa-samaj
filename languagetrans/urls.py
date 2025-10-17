from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('translate-page/', views.translate_page, name='translate_page'),
]
