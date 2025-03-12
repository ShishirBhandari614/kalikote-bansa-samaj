from django.urls import path
from .views import *
app_name = 'gallery'



urlpatterns = [
    path('photo-list/', user_list_view, name='usercustom_form_list'),
    path('photo-detail/<int:pk>/', user_detail_view, name='user_photo_details'),
    path('video-list/', user_videolist_view, name='uservideo-list'),
    path('base/', base, name='base'),
    path('video-detail/<int:pk>/', user_videodetail_view, name='uservideo-detail'),
]


