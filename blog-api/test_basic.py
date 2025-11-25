import requests

# Test the basic API endpoint first
url = "http://localhost:5000/api"

try:
    print(f"Testing GET to {url}")
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Basic API is working!")
        
        # Now test the register endpoint
        register_url = "http://localhost:5000/api/register"
        data = {
            "username": "testuser",
            "email": "test@example.com", 
            "password": "testpass123"
        }
        
        print(f"\nTesting POST to {register_url}")
        register_response = requests.post(register_url, json=data)
        
        print(f"Register Status Code: {register_response.status_code}")
        print(f"Register Response: {register_response.text}")
        
    else:
        print(f"❌ Basic API failed with status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend. Is the server running on port 5000?")
except Exception as e:
    print(f"❌ Error: {e}")
