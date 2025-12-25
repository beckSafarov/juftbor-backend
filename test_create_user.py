"""
Test script to create a user using the sample_user.json file.
Run this after starting the FastAPI server.
"""
import requests
import json

# Load the sample user data
with open('sample_user.json', 'r') as f:
    user_data = json.load(f)

# API endpoint
url = "http://localhost:8000/users"

# Make POST request
response = requests.post(url, json=user_data)

# Print results
print("Status Code:", response.status_code)
print("\nResponse:")
print(json.dumps(response.json(), indent=2))

if response.status_code == 201:
    print("\n✅ User created successfully!")
else:
    print("\n❌ Failed to create user")
