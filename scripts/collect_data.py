import os
import pandas as pd
from dotenv import load_dotenv
import requests
import time

# --- Part 1: Authentication & Configuration ---
print("Attempting to load GitHub token...")
load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("GitHub token not found...")
print("Successfully loaded GitHub token.")

# We will talk to the GraphQL API directly
headers = {"Authorization": f"bearer {github_token}"}
graphql_endpoint = "https://api.github.com/graphql"

# CONFIGURATION
TARGET_REPOS = [
    'microsoft/vscode', 'pandas-dev/pandas', 'ansible/ansible',
    'keras-team/keras', 'facebook/react', 'tensorflow/tensorflow',
    'flutter/flutter', 'kubernetes/kubernetes', 'elastic/elasticsearch',
    'docker/compose'
]
# We can use a larger number now because GraphQL is very fast
ISSUES_PER_REPO = 500 

LABEL_KEYWORDS = {
    'bug': ['bug', 'defect', 'error', 'issue'],
    'enhancement': ['enhancement', 'feature', 'feat', 'suggestion'],
    'documentation': ['documentation', 'docs'],
    'question': ['question', 'help', 'support']
}

# --- Part 2: The GraphQL Query ---
# This is our specific, efficient request to the API
graphql_query_template = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    issues(first: 100, after: $cursor, states: CLOSED, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        title
        body
        labels(first: 10) {
          nodes {
            name
          }
        }
      }
    }
  }
  rateLimit {
    remaining
  }
}
"""

# --- Part 3: The Smarter Filtering Logic ---
def find_matching_label(issue_labels):
    found_categories = set()
    for label in issue_labels:
        label_lower = label.lower()
        for category, keywords in LABEL_KEYWORDS.items():
            for keyword in keywords:
                if f' {keyword} ' in f' {label_lower} ' or label_lower == keyword:
                    found_categories.add(category)
    if len(found_categories) == 1:
        return found_categories.pop()
    return None

# --- Part 4: The High-Performance Data Collection Pipeline ---
all_issues_data = []
print("\nStarting data collection with high-performance GraphQL API...")

for repo_name in TARGET_REPOS:
    try:
        print(f"\nFetching issues from '{repo_name}'...")
        owner, name = repo_name.split('/')
        
        repo_matches = 0
        has_next_page = True
        cursor = None

        while has_next_page and repo_matches < ISSUES_PER_REPO:
            variables = {"owner": owner, "name": name, "cursor": cursor}
            response = requests.post(graphql_endpoint, json={'query': graphql_query_template, 'variables': variables}, headers=headers)
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                print(f"  -> GraphQL Errors: {data['errors']}")
                break

            issues_data = data['data']['repository']['issues']
            rate_limit = data['data']['rateLimit']

            for issue in issues_data['nodes']:
                if repo_matches >= ISSUES_PER_REPO:
                    break
                
                issue_labels_text = {label['name'] for label in issue['labels']['nodes']}
                matched_label = find_matching_label(issue_labels_text)

                if matched_label:
                    all_issues_data.append({
                        'title': issue['title'],
                        'body': issue['body'] or "",
                        'label': matched_label
                    })
                    repo_matches += 1
            
            print(f"  -> Scanned a page. Total matches for '{repo_name}': {repo_matches}")
            
            has_next_page = issues_data['pageInfo']['hasNextPage']
            cursor = issues_data['pageInfo']['endCursor']

            if rate_limit['remaining'] < 50:
                print("Approaching rate limit. Waiting for 15 minutes...")
                time.sleep(900)
        
        print(f"-> Finished '{repo_name}'. Found {repo_matches} relevant issues.")

    except Exception as e:
        print(f"Could not process repo {repo_name}. Error: {e}")

print(f"\nData collection complete. Total issues found: {len(all_issues_data)}.")

# --- Part 5: Saving the Final Dataset ---
print("Saving final dataset...")
if not os.path.exists('data'):
    os.makedirs('data')
df = pd.DataFrame(all_issues_data)
output_path = 'data/issues.csv'
df.to_csv(output_path, index=False)
print(f"Successfully saved new dataset to '{output_path}'")
print("\nPhase 1 is now truly complete!")