"""
QuickBite Connect - Payment URLs
"""
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment Intent
    path('create-intent/', views.CreatePaymentIntentView.as_view(), name='create-intent'),
    path('confirm/', views.ConfirmPaymentView.as_view(), name='confirm-payment'),
    
    # Payment History
    path('', views.PaymentListView.as_view(), name='payment-list'),
    path('<str:transaction_id>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    
    # Saved Cards
    path('cards/', views.PaymentCardListView.as_view(), name='card-list'),
    
    # Refunds
    path('refund/', views.RefundRequestView.as_view(), name='refund-request'),
]