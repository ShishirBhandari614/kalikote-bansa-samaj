from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.response import TemplateResponse
from.serializers import Photoserializer
from django.http import JsonResponse
from rest_framework import status
from .models import CustomForm



class add_photo(APIView):
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



def custom_form_list(request):
    forms = CustomForm.objects.all().order_by('-datetime')  # Sorting by datetime
    return render(request, 'gallerylist.html', {'forms': forms})


def custom_form_detail(request, pk):
    form = get_object_or_404(CustomForm, pk=pk)
    return render(request, 'gallerydetails.html', {'form': form})



class editphoto(APIView):
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
       
                
def delete_data(request, pk):
    query = CustomForm.objects.get(pk=pk)
    query.delete()
    return redirect("/admin/list/")
