import requests
import json
import time

# Base URL for the API
BASE_URL = 'http://localhost:5000/api'

def print_test_header(test_name):
    print(f"\n{'='*50}")
    print(f"TEST: {test_name}")
    print(f"{'='*50}")

def test_home():
    print_test_header("Home Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_register():
    print_test_header("User Registration")
    # Add timestamp to make username and email unique
    timestamp = int(time.time())
    user_data = {
        'username': f'testuser_{timestamp}',
        'email': f'test_{timestamp}@example.com',
        'password': 'testpass123'
    }
    print(f"Registering user: {user_data['username']}")
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        print("✅ Registration successful")
        return user_data, True
    else:
        print("❌ Registration failed")
        return None, False

def test_login(user_data):
    print_test_header("User Login")
    login_data = {
        'email': user_data['email'],
        'password': user_data['password']
    }
    print(f"Logging in user: {user_data['email']}")
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json().get('token')
        print("✅ Login successful")
        print(f"Token: {token[:20]}...")  # Print first 20 chars of token
        return token, True
    else:
        print("❌ Login failed")
        print(f"Response: {response.json()}")
        return None, False

def test_create_post(token):
    print_test_header("Create Post")
    headers = {'x-access-token': token}
    post_data = {
        'title': 'My First Post',
        'content': 'This is the content of my first post.'
    }
    print("Creating a new post...")
    response = requests.post(f"{BASE_URL}/posts", json=post_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        print("✅ Post created successfully")
        return True
    else:
        print("❌ Failed to create post")
        return False

def test_get_posts(token):
    print_test_header("Get All Posts")
    headers = {'x-access-token': token}
    print("Fetching all posts...")
    response = requests.get(f"{BASE_URL}/posts", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        posts = response.json()
        print(f"Found {len(posts)} posts:")
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']} by {post['author']}")
        print("✅ Successfully retrieved posts")
        return True
    else:
        print("❌ Failed to retrieve posts")
        print(f"Response: {response.json()}")
        return False

def run_tests():
    print("\n" + "="*60)
    print("STARTING API TESTS")
    print("="*60)
    
    # Initialize test results
    test_results = {}
    
    # Test 1: Home endpoint
    test_results['home'] = test_home()
    
    # Test 2: User registration
    user_data, registration_success = test_register()
    test_results['register'] = registration_success
    
    # Only continue if registration was successful
    if registration_success:
        # Test 3: User login
        token, login_success = test_login(user_data)
        test_results['login'] = login_success
        
        if login_success and token:
            # Test 4: Create a post
            test_results['create_post'] = test_create_post(token)
            
            # Test 5: Get all posts
            test_results['get_posts'] = test_get_posts(token)
    
    # Print test summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, success in test_results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name.upper().ljust(15)}: {status}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    run_tests()
