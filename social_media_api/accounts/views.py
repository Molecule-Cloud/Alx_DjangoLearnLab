from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from .models import CustomUser
from .serializers import *
from django.db.models import Q

# VIEWS TO HANDLE API REQUESTS FOR USER REGISTRATION, LOGIN, PROFILE MANAGEMENT, AND FOLLOWING/UNFOLLOWING USERS

class RegistrationView(generics.CreateAPIView):
    """
    View to create new users and return an authentication token upson success
    """
    # Query the CustomUserModel
    # Set the serializer to UserRegistrationSerializer
    # Allow any user (authenticated or not) to access this view

    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to register new users. Validate the data and return an auth token if successful
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.save()

        # Create token for the user
        token, created = Token.objects.get_or_create(user = user)
        
        return Response(
            {
                'user': UserProfileSerializer(user, context={'request': request}).data,
                'token': user.auth_token.key,
                'message': "Created Successfully"
            }, status=status.HTTP_201_CREATED
        )
    

# LOGIN VIEW API && AUTHENTATION TOKEN

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user) #Log the user in
        token, created = Token.objects.get_aor_create(user=user)

        return Response(
            {
                'user': UserProfileSerializer(user, context={'request': request}).data,
                'token': token.key,
                'message': "Login Successful"
            }, status=status.HTTP_200_OK
        )
    

# Logout View to Handle User Logout and Token Deletion
class LogoutView(APIView):
    def post(self, request):
        request.usr.auth_token.delete() # Delete the user's token to log them out
        logout(request)
        return Response(
            {
                'message': "You logged out"
            }, status=status.HTTP_200_OK
        )


# Profile View to Retrieve and Update User Profile Information

class Profile(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_profile(self):
        return self.request.user
    


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    # Optionally filter users by search query
    def filter_data(self):
        queryset = CustomUser.objects.all()
        serializer_class = UserProfileSerializer
        permission_classes = [permissions.AllowAny]



class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    def filter_search(self):
        query_set = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | 
                Q(email__icontains=search) | 
                Q(bio__icontains=search)
            )
        



class FollowUserView(APIView):
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)

            if user_to_follow == request.user:
                return Response(
                    {
                        'error': "You cannot follow yourself"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            if request.user.following.filter(id=user_id).exists():
                request.user.following.remove(user_to_follow)
                message = f"You unfollowed {user_to_follow.username}"
            else:
                request.user.following.add(user_to_follow)
                message = f"You started following {user_to_follow.username}"

            return Response(
                {
                    'message': message,
                    'followers_count': user_to_follow.followers_count
                }, status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {
                    'error': "User does not exist"
                }, status=status.HTTP_404_NOT_FOUND
            )