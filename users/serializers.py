"""
QuickBite Connect - User Serializers
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, CustomerProfile, Address


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'phone_number',
            'user_type', 'profile_image', 'is_email_verified', 
            'is_phone_verified', 'date_joined'
        )
        read_only_fields = ('id', 'date_joined', 'is_email_verified', 'is_phone_verified')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 
                  'phone_number', 'user_type')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        
        # Create customer profile if user type is customer
        if user.user_type == 'customer':
            CustomerProfile.objects.create(user=user)
        
        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serializer for Customer Profile"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ('id', 'loyalty_points', 'loyalty_tier', 'created_at', 'updated_at')


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""
    
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        # Set user from context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)