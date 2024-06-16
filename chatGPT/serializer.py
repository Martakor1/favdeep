
from .models import *
from rest_framework import serializers
class GptSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    class Meta:
        fields ='__all__'
class GptSerializerFilter(serializers.Serializer):
    message = serializers.CharField(required=True)
    category = serializers.JSONField(required=True)

    class Meta:
        fields ='__all__'
