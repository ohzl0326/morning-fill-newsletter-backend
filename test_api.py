#!/usr/bin/env python3
"""
Test script for The Morning Fill Newsletter API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running with: python3 app.py")
        return False

def test_subscribe():
    """Test the subscribe endpoint"""
    print("\n📝 Testing subscribe endpoint...")
    
    # Test data
    test_subscriber = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "Test Company",
        "job_title": "Developer",
        "consent_given": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/subscribe", json=test_subscriber)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running with: python3 app.py")
        return False

def test_duplicate_email():
    """Test duplicate email handling"""
    print("\n🔄 Testing duplicate email handling...")
    
    test_subscriber = {
        "email": "test@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "consent_given": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/subscribe", json=test_subscriber)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 409  # Should return conflict
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API")
        return False

def test_invalid_data():
    """Test invalid data handling"""
    print("\n⚠️  Testing invalid data handling...")
    
    # Test without email
    invalid_data = {
        "first_name": "John",
        "consent_given": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/subscribe", json=invalid_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400  # Should return bad request
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing The Morning Fill Newsletter API")
    print("=" * 50)
    
    # Check if server is running
    if not test_health():
        print("\n❌ API server is not running!")
        print("Please start the server with: python3 app.py")
        return
    
    # Run tests
    tests = [
        test_subscribe,
        test_duplicate_email,
        test_invalid_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"✅ Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")

if __name__ == "__main__":
    main() 