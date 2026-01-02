from rest_framework import serializers
from .models import AppLink

class AppLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppLink
        fields = '__all__'
