from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.http import JsonResponse
from django.template.response import TemplateResponse
# Create your views here.

def home(request):
    return render(request,"frontpage.html")


class ContactMessageView(APIView):
    def get(self, request):
        return TemplateResponse(request, 'samparka.html', {})

    def post(self, request):
        print(request.data)
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return a JSON response indicating success
            return JsonResponse({'message': 'Message sent successfully!'}, status=status.HTTP_200_OK)
        
        # If there are errors, return them in a JSON response
        return JsonResponse({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


