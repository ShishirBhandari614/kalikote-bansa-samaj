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
from gallery.views import add_photo
from django.urls import path, include
 # Import the custom admin site
import jazzmin
from django.conf import settings
from django.conf.urls.static import static
from gallery.views import custom_form_list, custom_form_detail, editphoto, delete_data

urlpatterns = [
    path('admin/add-photo/',add_photo.as_view(), name='add-photo'),  # Custom URL for the add-photo page
    path('admin/list/', custom_form_list, name='custom_form_list'),
    path('admin/detail/<int:pk>/', custom_form_detail, name='custom_form_detail'),
    path('admin/edit/<int:pk>/', editphoto.as_view(), name="edit_photo"),
    path('delete_data/<int:pk>/', delete_data, name="delete_data"),

    path('admin/', admin.site.urls),

    path('', include("core.urls")),
    # path('', include("gallery.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)