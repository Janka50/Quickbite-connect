"""
QuickBite Connect - API Endpoint Testing Script
Run this script to test if all APIs are working
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    
    print("🧪 Testing QuickBite Connect APIs\n")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Server Connection...")
    try:
        response = requests.get(f"{BASE_URL}/admin/")
        if response.status_code == 200 or response.status_code == 302:
            print("   ✅ Server is running!")
        else:
            print(f"   ❌ Server returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Server not running: {e}")
        return
    
    # Test 2: User Registration
    print("\n2. Testing User Registration API...")
    user_data = {
        "email": f"testuser{int(time.time())}@test.com",
        "password": "TestPass123!",
        "password2": "TestPass123!",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+1234567890",
        "user_type": "customer"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/users/register/", json=user_data)
        if response.status_code == 201:
            print("   ✅ User registration works!")
            print(f"   Created user: {response.json()['user']['email']}")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Store List API
    print("\n3. Testing Store List API...")
    try:
        response = requests.get(f"{BASE_URL}/api/stores/")
        if response.status_code == 200:
            stores = response.json()
            print(f"   ✅ Store list works! Found {stores.get('count', 0)} stores")
        else:
            print(f"   ❌ Store list failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Product Categories API
    print("\n4. Testing Product Categories API...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/categories/")
        if response.status_code == 200:
            print("   ✅ Product categories API works!")
        else:
            print(f"   ❌ Categories failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Product List API
    print("\n5. Testing Product List API...")
    try:
        response = requests.get(f"{BASE_URL}/api/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"   ✅ Product list works! Found {products.get('count', 0)} products")
        else:
            print(f"   ❌ Product list failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Testing Complete!\n")

if __name__ == "__main__":
    import time
    test_api_endpoints()