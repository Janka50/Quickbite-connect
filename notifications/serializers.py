"""
QuickBite Connect - Notification Serializers
"""
from rest_framework import serializers
from .models import Notification, NotificationPreference, PushToken


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notifications"""
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'read_at')


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for Notification Preferences"""
    
    class Meta:
        model = NotificationPreference
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class PushTokenSerializer(serializers.ModelSerializer):
    """Serializer for Push Tokens"""
    
    class Meta:
        model = PushToken
        fields = ('id', 'token', 'platform', 'device_id', 'is_active')
        read_only_fields = ('id', 'user')