import os
from dotenv import load_dotenv
from github import Github

print("--- GitHub API Diagnostic Script ---")

# Load the token from our .env file
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    raise ValueError("Token not found. Please check your .env file.")

print("Token loaded successfully. Authenticating...")

try:
    # Connect to the GitHub API
    g = Github(github_token)

    print("Authentication successful. Fetching rate limit object...")
    rate_limit_object = g.get_rate_limit()

    print("\n" + "="*50)
    print("OBJECT INSPECTION RESULTS:")
    print(f"Successfully fetched the object. Its type is: {type(rate_limit_object)}")

    # The dir() function gives us a list of everything inside the object
    print("\nHere are all the available attributes in the object:")
    print(dir(rate_limit_object))
    print("="*50)

    print("\nNow let's try to print the object itself to see its contents:")
    print(rate_limit_object)
    print("="*50)


except Exception as e:
    print(f"\nAn error occurred during the process: {e}")