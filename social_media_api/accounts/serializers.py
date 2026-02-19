from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser



class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles Creating new users with password validation
    """
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password],
        style = {'input_type': 'password'}
    )

    password2 = serializers.CharField(
        write_only = True,
        required = True,
        style = {'input_type': 'password'}
    )

    class Meta:

        model = CustomUser

        fields = ['id', 'username', 'email', 'password', 'password2', 'bio', 'profile_picture']

        extra_kwargs = {
            'email': {'required': True},
            'bio': {'required': False},
            'profile_picture': {'required': False}
        }

    def validate(self, attributes):
        """
        Validtion to check if both passwords match
        """
        if attributes['password'] != attributes['password2']:
            raise serializers.ValidationError({
                "password": "Password fields do not match."
            })
        elif attributes['password'].len() > attributes['password2'].len():
            raise serializers.ValidationError({
                "password": "Check the password lengths."
            })
        else:
            return attributes
        

    def create(self, validated_password):
        """
        Create and return a new user wiith encrypted password
        """
        validated_password.pop('password2')
        user = CustomUser.objects.create_user(**validated_password)
        return user

# USER LOGIN SERIALIZER

class UserLoginSerializer(serializers.Serilizer):
    """
        Validate Username and Password for user Login
    """
    username = serializers.CharFeild(
        required = True,
        write_only = True,
        style = {"input_type": "Password"}
    )

    def validate(self, attributes):
        """
        Validate and Authenticate the User
        """
        username = attributes.get('username')
        password = attributes.get('oasswird')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError("Error validating Credentials")
        else:
            raise serializers.ValidationError("Please provide username and password")

        attributes['user'] = user
        return attributes


# USER PROFILE SERIALIZER

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing/ipdating user profiles and follower following count
    """

    followers_count = serializers.IntegerField(read_only = True)
    following_count =  serializers.IntegerField(read_only = True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture',  'follwers_count', 'following_count', 'is_following', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_is_following(self, obj):
        """
        Check if the user follws this profile
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following.filter(id=obj.id).exists()
        return False

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing users
    """

    followers_count = serializers.IntegerField(read_only = True)

    class Meta:

        model = CustomUser

        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count']
          