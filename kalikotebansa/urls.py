"""
URL configuration for kalikotebansa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from gallery.views import add_photo, add_video, editvideo, admin_videodetail_view, admin_list_view, admin_detail_view, editphoto, delete_data, admin_videolist_view, video_data
from django.urls import path, include
 # Import the custom admin site
import jazzmin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/add-photo/',add_photo.as_view(), name='add-photo'),  
    path('admin/add-video/',add_video.as_view(), name='add-video'),  

    path('admin/photo-list/', admin_list_view, name='custom_form_list'),
    path('admin/video-list/', admin_videolist_view, name='video-list'),
    path('admin/photo-detail/<int:pk>/', admin_detail_view, name='custom_form_detail'),
    path('admin/video-detail/<int:pk>/', admin_videodetail_view, name='video-detail'),


    path('admin/edit-photo/<int:pk>/', editphoto.as_view(), name="edit_photo"),
    path('admin/edit-video/<int:pk>/', editvideo.as_view(), name="edit_video"),
    path('delete_data/<int:pk>/', delete_data, name="delete_data"),
    path('video-delete-data/<int:pk>/', video_data, name="video_delete_data"),
    path('', include("gallery.urls")),
    path('admin/', admin.site.urls),

    path('', include("core.urls")),
    # path('', include("gallery.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)