from django.contrib import admin

from gallery.models import *
admin.site.register(CustomForm)

admin.site.index_template = 'admin/adminindex.html'  # Ensure this loads your custom index template
