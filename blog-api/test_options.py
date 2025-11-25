import requests

# Check all available routes
url = "http://localhost:5000/api"

try:
    print(f"Testing GET to {url}")
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test OPTIONS to see allowed methods
    register_url = "http://localhost:5000/api/register"
    print(f"\nTesting OPTIONS to {register_url}")
    options_response = requests.options(register_url)
    
    print(f"OPTIONS Status Code: {options_response.status_code}")
    print(f"Allow Header: {options_response.headers.get('Allow', 'No Allow header')}")
    print(f"OPTIONS Response: {options_response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")
