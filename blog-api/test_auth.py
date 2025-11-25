import requests
import json
import random
import string

# Configuration
BASE_URL = "http://localhost:5000/api"

def generate_random_string(length=8):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def print_response(response, description):
    """Print the response in a formatted way"""
    print(f"\n{description}:")
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:", json.dumps(response.json(), indent=2))
    except:
        print("Response:", response.text)

def test_authentication():
    # Test data
    username = f"testuser_{generate_random_string(4)}"
    email = f"{username}@example.com"
    password = "Test@1234"
    
    print(f"\n{'='*50}")
    print("TESTING AUTHENTICATION SYSTEM")
    print(f"{'='*50}")
    
    # 1. Register a new user (should be assigned 'user' role by default)
    print("\n1. Registering a new user...")
    register_data = {
        'username': username,
        'email': email,
        'password': password
    }
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print_response(response, "Registration Response")
    
    if response.status_code != 201:
        print("Failed to register user. Exiting...")
        return
    
    # 2. Login with the new user
    print("\n2. Logging in with the new user...")
    login_data = {
        'email': email,
        'password': password
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print_response(response, "Login Response")
    
    if response.status_code != 200:
        print("Failed to login. Exiting...")
        return
    
    # Extract the auth token
    auth_token = response.json().get('token')
    if not auth_token:
        print("No token received. Exiting...")
        return
    
    headers = {
        'x-access-token': auth_token,
        'Content-Type': 'application/json'
    }
    
    # 3. Get current user info
    print("\n3. Getting current user info...")
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print_response(response, "Current User Info")
    
    # 4. Try to access admin-only endpoint (should fail with 403)
    print("\n4. Trying to access admin-only endpoint (should fail with 403)...")
    response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
    print_response(response, "Admin Users Endpoint (should fail with 403)")
    
    # 5. Create a new post (should work for regular users)
    print("\n5. Creating a new post...")
    post_data = {
        'title': 'My First Post',
        'content': 'This is a test post created by the test script.',
        'published': True
    }
    response = requests.post(f"{BASE_URL}/posts", json=post_data, headers=headers)
    print_response(response, "Create Post Response")
    
    if response.status_code == 201:
        post_id = response.json().get('id')
        
        # 6. Update the post (should work for the post author)
        print("\n6. Updating the post...")
        update_data = {
            'title': 'My Updated Post',
            'content': 'This post has been updated by the test script.',
            'published': True
        }
        response = requests.put(
            f"{BASE_URL}/posts/{post_id}", 
            json=update_data, 
            headers=headers
        )
        print_response(response, "Update Post Response")
        
        # 7. Delete the post (should work for the post author)
        print("\n7. Deleting the post...")
        response = requests.delete(
            f"{BASE_URL}/posts/{post_id}",
            headers=headers
        )
        print_response(response, "Delete Post Response")
    
    # 8. Logout (if implemented)
    print("\n8. Logging out...")
    # Note: Since we're using JWT, logging out is handled client-side by discarding the token
    # But we can test an endpoint that requires authentication to verify the token is valid
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print_response(response, "Current User Info After Logout")
    
    print("\nAuthentication testing completed!")

if __name__ == "__main__":
    test_authentication()
