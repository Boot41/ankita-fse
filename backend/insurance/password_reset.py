from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from .models import User

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@method_decorator(ratelimit(key='ip', rate='5/m', method=['POST']))
def request_password_reset(request):
    """Send password reset email to user."""
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Always return success to prevent email enumeration
        return Response({'detail': 'Password reset email sent if account exists.'})

    # Generate password reset token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Create reset link
    reset_url = f'{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}'
    
    # Send email
    send_mail(
        'Reset Your Password',
        f'Click the following link to reset your password: {reset_url}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    
    return Response({'detail': 'Password reset email sent if account exists.'})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@method_decorator(ratelimit(key='ip', rate='5/m', method=['POST']))
def reset_password(request):
    """Reset user password using token."""
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('password')
    
    if not all([uid, token, new_password]):
        return Response(
            {'error': 'Missing required fields'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Decode user id and get user
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        
        # Verify token
        if not default_token_generator.check_token(user, token):
            return Response(
                {'error': 'Invalid or expired token'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return Response({'detail': 'Password reset successful.'})
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {'error': 'Invalid reset link'},
            status=status.HTTP_400_BAD_REQUEST
        )
