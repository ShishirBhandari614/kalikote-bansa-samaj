from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from gallery.models import CustomForm  # Only import the necessary model
from core.models import ContactMessage

from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = "My Custom Admin Header"
    site_title = "My Custom Site Title"
    index_title = "Welcome to My Admin Portal"

admin_site = MyAdminSite(name='myadmin')

class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        # Find the "Gallery" app and add custom links
        for app in app_list:
            if app["name"] == "Gallery":  # Adjust based on your app name
                app["models"].append({
                    "name": "📸 Add Photo",
                    "object_name": "Add Photo",
                    "admin_url": reverse("add-photo"),
                    "view_only": True
                })
                app["models"].append({
                    "name": "🖼 Photo List",
                    "object_name": "Photo List",
                    "admin_url": reverse("custom_form_list"),
                    "view_only": True
                })
                app["models"].append({
                    "name": "🎥 Add Video",
                    "object_name": "Add Video",
                    "admin_url": reverse("add-video"),
                    "view_only": True
                })
                app["models"].append({
                    "name": "📂 Video List",
                    "object_name": "Video List",
                    "admin_url": reverse("video-list"),
                    "view_only": False
                })
                app["models"].append({
                    "name": "create admin",
                    "object_name": "create admin",
                    "admin_url": reverse("create_superuser"),
                    "view_only": False
                })
                break  # Stop looping once "Gallery" is found

        return app_list

# Create a custom admin instance
admin_site = CustomAdminSite(name="custom_admin")

# Register only specific models
admin_site.register(CustomForm)  # Register only the "Gallery" model
admin_site.register(ContactMessage)

admin_site.site_header = "Kalikote Bansha Samaj"
