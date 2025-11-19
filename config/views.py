"""
QuickBite Connect - System Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.conf import settings
import sys


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """API health check endpoint"""
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return Response({
        'status': 'healthy',
        'service': 'QuickBite Connect API',
        'version': '1.0.0',
        'environment': settings.DEBUG and 'development' or 'production',
        'python_version': sys.version,
        'database': db_status,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """API information endpoint"""
    
    return Response({
        'name': 'QuickBite Connect API',
        'version': '1.0.0',
        'description': 'Food and Grocery Delivery Platform API',
        'documentation': {
            'swagger': request.build_absolute_uri('/api/docs/'),
            'redoc': request.build_absolute_uri('/api/redoc/'),
            'schema': request.build_absolute_uri('/api/schema/'),
        },
        'endpoints': {
            'users': '/api/users/',
            'stores': '/api/stores/',
            'products': '/api/products/',
            'orders': '/api/orders/',
            'payments': '/api/payments/',
            'reviews': '/api/reviews/',
            'notifications': '/api/notifications/',
        }
    })