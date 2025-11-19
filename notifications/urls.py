"""
QuickBite Connect - Notification URLs
"""
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Notifications
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('unread-count/', views.UnreadNotificationCountView.as_view(), name='unread-count'),
    path('<uuid:notification_id>/read/', views.MarkNotificationReadView.as_view(), name='mark-read'),
    path('mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark-all-read'),
    path('<uuid:notification_id>/delete/', views.DeleteNotificationView.as_view(), name='delete-notification'),
    
    # Preferences
    path('preferences/', views.NotificationPreferenceView.as_view(), name='preferences'),
    
    # Push Tokens
    path('push-token/register/', views.RegisterPushTokenView.as_view(), name='register-push-token'),
]