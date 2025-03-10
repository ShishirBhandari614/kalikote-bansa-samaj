from rest_framework import serializers
from .models import CustomForm

class Photoserializer(serializers.ModelSerializer):
    class Meta:
        model = CustomForm
        fields = '__all__'
