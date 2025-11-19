from django.shortcuts import render
"""
QuickBite Connect - Notification Views
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Notification, NotificationPreference, PushToken
from .serializers import (
    NotificationSerializer,
    NotificationPreferenceSerializer,
    PushTokenSerializer
)
from .services import NotificationService


class NotificationListView(generics.ListAPIView):
    """API endpoint to list user's notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class UnreadNotificationCountView(APIView):
    """API endpoint to get unread notification count"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = NotificationService.get_unread_count(request.user)
        return Response({'unread_count': count})


class MarkNotificationReadView(APIView):
    """API endpoint to mark notification as read"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            user=request.user
        )
        notification.mark_as_read()
        return Response({
            'message': 'Notification marked as read',
            'notification': NotificationSerializer(notification).data
        })


class MarkAllNotificationsReadView(APIView):
    """API endpoint to mark all notifications as read"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        NotificationService.mark_all_as_read(request.user)
        return Response({'message': 'All notifications marked as read'})


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """API endpoint to get/update notification preferences"""
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        obj, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return obj


class RegisterPushTokenView(generics.CreateAPIView):
    """API endpoint to register push notification token"""
    serializer_class = PushTokenSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        # Check if token already exists
        token = request.data.get('token')
        existing_token = PushToken.objects.filter(token=token).first()
        
        if existing_token:
            # Update user if different
            if existing_token.user != request.user:
                existing_token.user = request.user
                existing_token.is_active = True
                existing_token.save()
            return Response({
                'message': 'Push token updated',
                'token': PushTokenSerializer(existing_token).data
            })
        
        # Create new token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_obj = serializer.save(user=request.user)
        
        return Response({
            'message': 'Push token registered',
            'token': PushTokenSerializer(token_obj).data
        }, status=status.HTTP_201_CREATED)


class DeleteNotificationView(APIView):
    """API endpoint to delete notification"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            id=notification_id,
            user=request.user
        )
        notification.delete()
        return Response({'message': 'Notification deleted'})
