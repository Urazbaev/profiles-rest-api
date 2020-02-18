from rest_framework import serializers
from profiles_api import models

# Serializes a name field for testing our APIView
class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)

# Serializes a user profile object
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    # Create and return a new user
    def create(self,validated_data):
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user
