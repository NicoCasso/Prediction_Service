import json
import requests

# Base URL of your FastAPI server
base_url = "http://127.0.0.1:8000"

# Authentication token (ensure you have a valid token from the `/auth/login` endpoint)
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtaWtlQHRlc3QuY29tIiwiaWQiOjEsImV4cCI6MTc0MDY4NjI4OX0.2o_DGCzqaif6PPtlW3CyjeasEa3t3psIC3c37toQMfg"

# Loan request data
loan_request_data = {
    "state": "CA",
    "bank": "CAPITAL ONE NATL ASSOC",
    "naics": 55,
    "term": 12,
    "no_emp": 12,
    "new_exist": 1,
    "create_job": 4,
    "retained_job": 3,
    "urban_rural": 0,
    "rev_line_cr": 1,
    "low_doc": 1,
    "gr_appv": 90000,
    "recession": 1,
    "has_franchise": 1
}

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {auth_token}"
}

# Send POST request to the `/loans/request` endpoint
response = requests.post(
    f"{base_url}/loans/request",
    json=loan_request_data,
    headers=headers
)

# Print the response
print("Loan Request Response:")
print(response.json())