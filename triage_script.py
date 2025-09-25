# triage_script.py
import os
import requests
import json

print("--- Starting Triage Script ---")

# 1. Get all environment variables
issue_title = os.getenv("ISSUE_TITLE")
issue_body = os.getenv("ISSUE_BODY")
issue_number = os.getenv("ISSUE_NUMBER")
api_url = os.getenv("TRIAGE_API_URL")
github_token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")

# Check if variables are loaded
if not all([issue_title, issue_body, issue_number, api_url, github_token, repo_name]):
    print("Error: One or more environment variables are missing.")
    exit(1)

print(f"Processing Issue #{issue_number} in repo {repo_name}")

# 2. Call our prediction API
try:
    payload = json.dumps({"title": issue_title, "body": issue_body})
    headers = {"Content-Type": "application/json"}
    print(f"Sending payload to API: {api_url}")
    api_response = requests.post(api_url, headers=headers, data=payload, timeout=60)
    api_response.raise_for_status()
    predicted_label = api_response.json().get('predicted_label')
    print(f"API returned predicted label: '{predicted_label}'")
except Exception as e:
    print(f"Error calling the prediction API: {e}")
    exit(1)

# 3. Apply the label using the GitHub API
if predicted_label:
    try:
        labels_url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}/labels"
        auth_headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        label_payload = json.dumps({"labels": [predicted_label]})
        
        print(f"Applying label '{predicted_label}' to issue #{issue_number} via URL: {labels_url}")
        label_response = requests.post(labels_url, headers=auth_headers, data=label_payload, timeout=60)
        label_response.raise_for_status()
        
        print("--- Label applied successfully! ---")
    except Exception as e:
        print(f"Error applying label to the GitHub issue: {e}")
        # Print the response from GitHub API if there's an error
        if 'label_response' in locals():
            print(f"GitHub API response: {label_response.text}")
        exit(1)
else:
    print("No valid label was predicted. Exiting.")