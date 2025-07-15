from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.response import TemplateResponse
from.serializers import Photoserializer, videoserializer
from django.http import JsonResponse
from rest_framework import status
from .models import CustomForm,videoform
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages

class add_video(LoginRequiredMixin, APIView):
    def get(self, request):
        return TemplateResponse(request, 'addvideo.html', {})

    def post(self, request):
        print(request.data)
        serializer = videoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return a JSON response indicating success
            return JsonResponse({'message': 'photo added successfully!'}, status=status.HTTP_200_OK)
        
        # If there are errors, return them in a JSON response
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class add_photo(LoginRequiredMixin, APIView):
    def get(self, request):
        return TemplateResponse(request, 'addphoto.html', {})

    def post(self, request):
        print(request.data)
        serializer = Photoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return a JSON response indicating success
            return JsonResponse({'message': 'photo added successfully!'}, status=status.HTTP_200_OK)
        
        # If there are errors, return them in a JSON response
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@login_required
def admin_list_view(request):
    forms = CustomForm.objects.all().order_by('-datetime')  # Sorting by datetime
    return render(request, 'gallerylist.html', {'forms': forms})

@login_required
def admin_detail_view(request, pk):
    form = get_object_or_404(CustomForm, pk=pk)
    return render(request, 'gallerydetails.html', {'form': form})



# def user_list_view(request):
#     forms = CustomForm.objects.all().order_by('-datetime')  # Sorting by datetime
#     base_template = "admin/base_site.html" if request.user.is_staff else "base.html"
    
#     return render(request, 'gallerylist.html', {'forms': forms, 'base_template': base_template})


def user_list_view(request):
    forms = CustomForm.objects.all().order_by('-datetime')  # Sorting by datetime
    return render(request, 'usergallery.html', {'forms': forms})

def user_detail_view(request, pk):
    form = get_object_or_404(CustomForm, pk=pk)
    return render(request, 'usergallerydetails.html', {'form': form})
@login_required
def admin_videolist_view(request):
    forms = videoform.objects.all().order_by('-datetime')  # Sorting by datetime
    return render(request, 'videolist.html', {'forms': forms})


@login_required
def admin_videodetail_view(request, pk):
    form = get_object_or_404(videoform, pk=pk)
    return render(request, 'videodetail.html', {'form': form})

def user_videolist_view(request):
    forms = videoform.objects.all().order_by('-datetime')  # Sorting by datetime
    return render(request, 'uservideolist.html', {'forms': forms})

def user_videodetail_view(request, pk):
    form = get_object_or_404(videoform, pk=pk)
    return render(request, 'uservideodetail.html', {'form': form})

class editphoto(LoginRequiredMixin, APIView):
    def get(self, request, pk):
        form = get_object_or_404(CustomForm, pk=pk)
        context = {'form': form}
        return render(request, "editphoto.html", context)# Get the existing photo object

    def post(self, request, pk): 
        form = get_object_or_404(CustomForm, pk=pk)
        serializer = Photoserializer(instance=form, data=request.data)  # Update existing data
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Photo updated successfully!'}, status=status.HTTP_200_OK)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return render(request, "editphoto.html", context)
    

class editvideo(LoginRequiredMixin, APIView):
    def get(self, request, pk):
        form = get_object_or_404(videoform, pk=pk)
        context = {'form': form}
        return render(request, "editphoto.html", context)# Get the existing photo object

    def post(self, request, pk): 
        form = get_object_or_404(videoform, pk=pk)
        serializer = Photoserializer(instance=form, data=request.data)  # Update existing data
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Photo updated successfully!'}, status=status.HTTP_200_OK)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return render(request, "editphoto.html", context)

       
@login_required                
def delete_data(request, pk):
    query = CustomForm.objects.get(pk=pk)
    query.delete()
    return redirect("/admin/photo-list/")

@login_required                
def video_data(request, pk):
    query = videoform.objects.get(pk=pk)
    query.delete()
    return redirect("/admin/video-list/")


def base(request):
    return render(request,"base.html")

@method_decorator(staff_member_required, name='dispatch')
class AddVideoView(TemplateView):
    template_name = 'admin/addvideo.html'  # Must be in admin/ subdirectory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add admin-required context
        context.update({
            **self.admin_site.each_context(self.request),
            'title': 'Add Video',
            'opts': self.model._meta if hasattr(self, 'model') else None,
        })
        return context

    def post(self, request):
        serializer = videoserializer(data=request.POST, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Video added successfully!'}, status=status.HTTP_200_OK)
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@login_required
def create_superuser(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(request, "create_superuser.html", {"error": "Passwords do not match!"})

        if User.objects.filter(username=username).exists():
            return render(request, "create_superuser.html", {"error": "Username already taken!"})

        if User.objects.filter(email=email).exists():
            return render(request, "create_superuser.html", {"error": "Email already registered!"})

        # Create superuser
        user = User.objects.create_superuser(username=username, email=email, password=password)
        messages.success(request, "Superuser created successfully!")
        return redirect("/admin/create-superuser/")  # Redirect to Django admin login page

    return render(request, "create_superuser.html")