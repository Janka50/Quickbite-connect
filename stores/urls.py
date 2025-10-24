"""
QuickBite Connect - Store URLs
"""
from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('', views.StoreListView.as_view(), name='store-list'),
    path('create/', views.StoreCreateView.as_view(), name='store-create'),
    path('my-stores/', views.MyStoresView.as_view(), name='my-stores'),
    path('categories/', views.StoreCategoryListView.as_view(), name='category-list'),
    path('<slug:slug>/', views.StoreDetailView.as_view(), name='store-detail'),
    path('<uuid:pk>/update/', views.StoreUpdateView.as_view(), name='store-update'),
    path('<uuid:store_id>/staff/', views.StoreStaffListView.as_view(), name='store-staff'),
]