from rest_framework import serializers

# Serializes a name field for testing our APIView
class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)
    
