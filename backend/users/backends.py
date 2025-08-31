from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email address.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Handle both username and email parameters
        email = kwargs.get('email', username)
        
        if not email or not password:
            return None
        
        try:
            # Check if the email field is actually an email
            if '@' in email:
                user = User.objects.get(email=email)
            else:
                # Fallback to username if no email is provided
                user = User.objects.get(username=email)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
