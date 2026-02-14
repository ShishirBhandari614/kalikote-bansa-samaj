from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', role_login, name='role_login'),
    path('dashboard/', dashboard, name='dashboard'),  # Example dashboard path
    path('add_photo/', add_photo, name='add_photo'),  # Placeholder
    path('add_video/', add_video, name='add_video'),  # Placeholder
    path('change_password/', change_password, name='change_password'),  # Placeholder
    path('change_email/', change_email, name='change_email'),  # Placeholder
    path('logout/', logout, name='logout'),  # Placeholder
    path('manage_photos/', manage_photos, name='manage_photo'),  # Placeholder
    path('manage_videos/', manage_videos, name='manage_video'),  #
    path('edit_photo/<int:photo_id>/', edit_photo, name='edit_photo'),  # Placeholder
    path('edit_video/<int:video_id>/', edit_video, name='edit_video'),  # Placeholder   
    path('delete_photo/<int:photo_id>/', delete_photo, name='delete_photo'),  # Placeholder
    path('delete_video/<int:video_id>/', delete_video, name='delete_video'),  # Placeholder
    path('change_logo/', change_logo, name='change_logo'),
    path('add_members/', add_member, name='add_members'),
    path('add_slides/', add_slide, name='add_slides'),
    path('edit_slide/<int:slide_id>/', edit_slide, name='edit_slide'),
    path('delete_slide/<int:slide_id>/', delete_slide, name='delete_slide'),
    path('manage_slides/', manage_slides, name='manage_slide'),
    path('search_slides/', search_slides, name='search_slides'),
    path('manage_members/', manage_members, name='manage_members'),
    path('delete_member/<int:member_id>/', delete_member, name='delete_member'),
    path('edit_member/<int:member_id>/', edit_member, name='edit_member'),
    path('membership-list/', membership_list, name='membership_list'),
    path('membership/<int:pk>/', membership_detail, name='membership_detail'),
]