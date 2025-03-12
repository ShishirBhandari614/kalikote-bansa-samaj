from rest_framework import serializers
from .models import CustomForm, videoform

class Photoserializer(serializers.ModelSerializer):
    class Meta:
        model = CustomForm
        fields = '__all__'


class videoserializer(serializers.ModelSerializer):
    class Meta:
        model = videoform
        fields = '__all__'

