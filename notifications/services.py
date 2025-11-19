"""
QuickBite Connect - Notification Services
Email and SMS sending logic
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from twilio.rest import Client
from .models import Notification, EmailLog, SMSLog, NotificationPreference


class NotificationService:
    """Service for creating in-app notifications"""
    
    @staticmethod
    def create_notification(user, notification_type, title, message, related_object_id=None, related_object_type=None, action_url=''):
        """Create an in-app notification"""
        try:
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                related_object_id=related_object_id,
                related_object_type=related_object_type,
                action_url=action_url
            )
            return {'success': True, 'notification': notification}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_unread_count(user):
        """Get unread notification count for user"""
        return Notification.objects.filter(user=user, is_read=False).count()
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for user"""
        Notification.objects.filter(user=user, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )


class EmailService:
    """Service for sending emails"""
    
    @staticmethod
    def send_email(recipient_email, subject, message, html_message=None, email_type='', user=None, related_object_id=None):
        """Send email and log it"""
        
        # Create email log
        email_log = EmailLog.objects.create(
            user=user,
            recipient_email=recipient_email,
            subject=subject,
            body=message,
            html_body=html_message or '',
            email_type=email_type,
            related_object_id=related_object_id,
            status='pending'
        )
        
        try:
            # Check user preferences
            if user:
                prefs = NotificationPreference.objects.filter(user=user).first()
                if prefs and email_type == 'promotion' and not prefs.email_promotions:
                    email_log.status = 'skipped'
                    email_log.error_message = 'User opted out of promotional emails'
                    email_log.save()
                    return {'success': False, 'error': 'User opted out'}
            
            # Send email
            if html_message:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient_email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send()
            else:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient_email],
                    fail_silently=False
                )
            
            # Update log
            email_log.status = 'sent'
            email_log.sent_at = timezone.now()
            email_log.save()
            
            return {'success': True, 'email_log': email_log}
            
        except Exception as e:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def send_order_confirmation(order):
        """Send order confirmation email"""
        subject = f"Order Confirmation - {order.order_number}"
        message = f"""
        Dear {order.customer.full_name},
        
        Your order has been confirmed!
        
        Order Number: {order.order_number}
        Total Amount: ${order.total_amount}
        Estimated Delivery: {order.estimated_delivery_time}
        
        Thank you for shopping with QuickBite Connect!
        """
        
        return EmailService.send_email(
            recipient_email=order.customer.email,
            subject=subject,
            message=message,
            email_type='order_confirmation',
            user=order.customer,
            related_object_id=order.id
        )
    
    @staticmethod
    def send_order_status_update(order, new_status):
        """Send order status update email"""
        status_messages = {
            'confirmed': 'Your order has been confirmed!',
            'preparing': 'Your order is being prepared!',
            'ready': 'Your order is ready for pickup!',
            'out_for_delivery': 'Your order is out for delivery!',
            'delivered': 'Your order has been delivered!',
            'cancelled': 'Your order has been cancelled.'
        }
        
        subject = f"Order Update - {order.order_number}"
        message = f"""
        Dear {order.customer.full_name},
        
        {status_messages.get(new_status, 'Your order status has been updated.')}
        
        Order Number: {order.order_number}
        Status: {new_status.replace('_', ' ').title()}
        
        Track your order: [Order Tracking Link]
        
        Thank you for shopping with QuickBite Connect!
        """
        
        return EmailService.send_email(
            recipient_email=order.customer.email,
            subject=subject,
            message=message,
            email_type='order_update',
            user=order.customer,
            related_object_id=order.id
        )
    
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new user"""
        subject = "Welcome to QuickBite Connect!"
        message = f"""
        Dear {user.full_name or user.email},
        
        Welcome to QuickBite Connect!
        
        We're excited to have you join our community of food lovers.
        
        Start exploring amazing stores and delicious food near you!
        
        Best regards,
        The QuickBite Team
        """
        
        return EmailService.send_email(
            recipient_email=user.email,
            subject=subject,
            message=message,
            email_type='welcome',
            user=user
        )


class SMSService:
    """Service for sending SMS via Twilio"""
    
    @staticmethod
    def send_sms(recipient_phone, message, sms_type='', user=None, related_object_id=None):
        """Send SMS and log it"""
        
        # Create SMS log
        sms_log = SMSLog.objects.create(
            user=user,
            recipient_phone=recipient_phone,
            message=message,
            sms_type=sms_type,
            related_object_id=related_object_id,
            status='pending'
        )
        
        try:
            # Check user preferences
            if user:
                prefs = NotificationPreference.objects.filter(user=user).first()
                if prefs and sms_type == 'promotion' and not prefs.sms_promotions:
                    sms_log.status = 'skipped'
                    sms_log.error_message = 'User opted out of promotional SMS'
                    sms_log.save()
                    return {'success': False, 'error': 'User opted out'}
            
            # Initialize Twilio client
            if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
                raise Exception("Twilio credentials not configured")
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Send SMS
            sms_message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=recipient_phone
            )
            
            # Update log
            sms_log.status = 'sent'
            sms_log.twilio_sid = sms_message.sid
            sms_log.twilio_status = sms_message.status
            sms_log.sent_at = timezone.now()
            sms_log.save()
            
            return {'success': True, 'sms_log': sms_log}
            
        except Exception as e:
            sms_log.status = 'failed'
            sms_log.error_message = str(e)
            sms_log.save()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def send_order_update_sms(order, status):
        """Send order status update via SMS"""
        message = f"QuickBite: Your order {order.order_number} is now {status.replace('_', ' ')}. Track: [link]"
        
        return SMSService.send_sms(
            recipient_phone=order.customer.phone_number,
            message=message,
            sms_type='order_update',
            user=order.customer,
            related_object_id=order.id
        )
    
    @staticmethod
    def send_delivery_sms(order):
        """Send delivery notification SMS"""
        message = f"QuickBite: Your order {order.order_number} is out for delivery! Expected in {order.estimated_delivery_time} minutes."
        
        return SMSService.send_sms(
            recipient_phone=order.customer.phone_number,
            message=message,
            sms_type='delivery_update',
            user=order.customer,
            related_object_id=order.id
        )