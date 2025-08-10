from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, LoginSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Users in the public schema.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """if self.action in ['list', 'retrieve','create', 'login']:"""
        return [AllowAny()]
        """return [IsAuthenticated()]"""
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Login endpoint for users.
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        })
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Logout endpoint for users.
        """
        logout(request)
        return Response({'message': 'Logout successful'})
    
    @action(detail=False)
    def profile(self, request):
        """
        Get current user's profile.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False)
    def center_users(self, request):
        """
        Get users belonging to the same center as the current user.
        """
        if not request.user.center:
            return Response({'error': 'User is not associated with any center'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        users = User.objects.filter(center=request.user.center)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)