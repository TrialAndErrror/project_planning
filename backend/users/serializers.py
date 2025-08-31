from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer, LoginSerializer

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')
        
        attrs['user'] = user
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('id',) 