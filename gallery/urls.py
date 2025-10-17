from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import *
from django.conf.urls.static import static

urlpatterns = [
   path('photos/',photo_gallery,name='photo_gallery'),

   path('videos/',video_gallery,name='video_gallery'),
   path('contact/',contact_us,name='contact_us'),
   path('messages/',get_message,name='messages'),
   path('messages/delete/<int:message_id>/', delete_message, name='delete_message'),
   path('sahayog/', help, name='help'),
   path('help_list', help_list, name='help_list'),
   path ('notice_post/', notice_post, name='notice_post'),
   path('notice_list/', notice_list, name='notice_list'),
]
