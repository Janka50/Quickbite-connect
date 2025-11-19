"""
QuickBite Connect - Comprehensive API Testing Script
Tests all major API endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
test_results = []

def log_test(test_name, passed, message=""):
    """Log test results"""
    status = "✅ PASS" if passed else "❌ FAIL"
    test_results.append({
        'test': test_name,
        'passed': passed,
        'message': message
    })
    print(f"{status} - {test_name}")
    if message and not passed:
        print(f"   Error: {message}")

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        log_test("Health Check", response.status_code == 200, response.json().get('status'))
        return response.status_code == 200
    except Exception as e:
        log_test("Health Check", False, str(e))
        return False

def test_api_info():
    """Test API info endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/")
        log_test("API Info", response.status_code == 200)
        return response.status_code == 200
    except Exception as e:
        log_test("API Info", False, str(e))
        return False

def test_user_registration():
    """Test user registration"""
    try:
        timestamp = int(datetime.now().timestamp())
        user_data = {
            "email": f"test{timestamp}@test.com",
            "password": "TestPass123!",
            "password2": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+1234567890",
            "user_type": "customer"
        }
        response = requests.post(f"{BASE_URL}/api/users/register/", json=user_data)
        log_test("User Registration", response.status_code == 201)
        return response.json() if response.status_code == 201 else None
    except Exception as e:
        log_test("User Registration", False, str(e))
        return None

def test_store_list():
    """Test store listing"""
    try:
        response = requests.get(f"{BASE_URL}/api/stores/")
        log_test("Store List", response.status_code == 200)
        data = response.json()
        print(f"   Found {data.get('count', 0)} stores")
        return response.status_code == 200
    except Exception as e:
        log_test("Store List", False, str(e))
        return False

def test_store_categories():
    """Test store categories"""
    try:
        response = requests.get(f"{BASE_URL}/api/stores/categories/")
        log_test("Store Categories", response.status_code == 200)
        return response.status_code == 200
    except Exception as e:
        log_test("Store Categories", False, str(e))
        return False

def test_product_list():
    """Test product listing"""
    try:
        response = requests.get(f"{BASE_URL}/api/products/")
        log_test("Product List", response.status_code == 200)
        data = response.json()
        print(f"   Found {data.get('count', 0)} products")
        return response.status_code == 200
    except Exception as e:
        log_test("Product List", False, str(e))
        return False

def test_product_categories():
    """Test product categories"""
    try:
        response = requests.get(f"{BASE_URL}/api/products/categories/")
        log_test("Product Categories", response.status_code == 200)
        return response.status_code == 200
    except Exception as e:
        log_test("Product Categories", False, str(e))
        return False

def test_api_documentation():
    """Test API documentation endpoints"""
    try:
        # Test Swagger UI
        response = requests.get(f"{BASE_URL}/api/docs/")
        swagger_ok = response.status_code == 200
        
        # Test ReDoc
        response = requests.get(f"{BASE_URL}/api/redoc/")
        redoc_ok = response.status_code == 200
        
        # Test Schema
        response = requests.get(f"{BASE_URL}/api/schema/")
        schema_ok = response.status_code == 200
        
        all_ok = swagger_ok and redoc_ok and schema_ok
        log_test("API Documentation", all_ok)
        return all_ok
    except Exception as e:
        log_test("API Documentation", False, str(e))
        return False

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("🧪 QuickBite Connect - Comprehensive API Tests")
    print("="*60 + "\n")
    
    # Test if server is running
    print("1️⃣  Testing Server Connection...")
    if not test_health_check():
        print("\n❌ Server is not running! Please start the server first.")
        print("   Run: python manage.py runserver")
        return
    
    print("\n2️⃣  Testing Core Endpoints...")
    test_api_info()
    
    print("\n3️⃣  Testing User Management...")
    test_user_registration()
    
    print("\n4️⃣  Testing Store APIs...")
    test_store_list()
    test_store_categories()
    
    print("\n5️⃣  Testing Product APIs...")
    test_product_list()
    test_product_categories()
    
    print("\n6️⃣  Testing API Documentation...")
    test_api_documentation()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for t in test_results if t['passed'])
    failed_tests = total_tests - passed_tests
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests > 0:
        print("\n❌ Failed Tests:")
        for result in test_results:
            if not result['passed']:
                print(f"   - {result['test']}: {result['message']}")
    
    print("\n" + "="*60)
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Your API is working perfectly!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_tests()