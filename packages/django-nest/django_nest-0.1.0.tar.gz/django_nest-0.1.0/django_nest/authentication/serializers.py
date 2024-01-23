from rest_framework import serializers

class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
