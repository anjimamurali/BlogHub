import requests
import json

# Test the register endpoint
url = "http://localhost:5000/api/register"
data = {
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "testpass123"
}

try:
    print(f"Testing POST to {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 201:
        print("✅ Registration endpoint is working!")
    else:
        print(f"❌ Registration failed with status {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend. Is the server running on port 5000?")
except Exception as e:
    print(f"❌ Error: {e}")
