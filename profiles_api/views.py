from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from profiles_api import serializers, models, permissions


# Test API View
class HelloApiView(APIView):
    serializer_class = serializers.HelloSerializer

    # Returns a list of APIView features
    def get(self, request, format=None):
        an_apiview = [
                        'Uses HTTP methods as function ( get,post, patch, put, delete)',
                        'Is similar to a traditional Django View',
                        'Gives you the most control over you application logic',
                        'Is mapped manually to URLs',
                    ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    # Create a hello message with our name
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle updating an object
    def put(self, request, pk=None):
        return Response({'method': 'PUT'})

    # Handle a partial update of an object
    def patch(self, request, pk=None):
        return Response({'method': 'PATCH'})

    # Delete an object
    def delete(self, request, pk=None):
        return Response({'method': 'DELETE'})

# Test API ViewSet
class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializer

    # return a hello message
    def list(self, request):
        a_viewset = [
            'User actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    # Create a new hello message
    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    # Handle getting an object by it's ID
    def retrieve(self, request, pk=None):
        return Response({'http_method': 'GET'})

    # Handle updating an object
    def update(self, request, pk=None):
        return Response({'http_method': 'PUT'})

    # Handle updating part of an object
    def partial_update(self, request, pk=None):
        return Response({'http_method': 'PATCH'})

    # Handle removing and object
    def destroy(self, request, pk=None):
        return Response({'http_method': 'DELETE'})

# Handle creating and updating profiles
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

# Handle creating user authentication tokens
class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# Handles creating, reading and updating profile feed items
class UserProfileFeddViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus,IsAuthenticated)

    # Sets the user profile to the logged in user
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)
