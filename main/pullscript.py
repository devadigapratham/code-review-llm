import requests
import os
import json

# Set up headers with authorization
# Set your GitHub personal access token here
token = "github_token"

# Set up headers with authorization token
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'token {token}',
}

def search_go_repositories():
    url = 'https://api.github.com/search/repositories'
    params = {'q': 'language:go', 'per_page': 50}  # Limit to 50 repositories
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        print(f"Failed to search repositories: {response.status_code} - {response.text}")
        print(f"Rate Limit Remaining: {response.headers.get('X-RateLimit-Remaining')}")
        return []

def get_pull_request_count(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repo_data = response.json()
        return repo_data.get('open_issues_count', 0)  # Open issues count includes pull requests
    else:
        print(f"Failed to get repository info for {owner}/{repo}: {response.status_code} - {response.text}")
        return 0

def get_pull_requests(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
    params = {'state': 'all', 'per_page': 100}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get pull requests for {owner}/{repo}: {response.status_code} - {response.text}")
        return []

def get_review_comments(owner, repo, pull_number):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/comments'
    params = {'per_page': 100}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get review comments for PR #{pull_number} in {owner}/{repo}: {response.status_code} - {response.text}")
        return []

def main():
    go_repos = search_go_repositories()[:50]  # Limit to 50 repositories
    processed_repos = []
    batch_size = 10
    batch_data = []

    for repo in go_repos:
        owner = repo['owner']['login']
        repo_name = repo['name']
        
        pr_count = get_pull_request_count(owner, repo_name)
        
        if 10 <= pr_count <= 50:
            pull_requests = get_pull_requests(owner, repo_name)
            if not pull_requests:
                continue  # No pull requests found, move to the next repository

            repo_data = {
                "owner": owner,
                "repo_name": repo_name,
                "pull_requests": []
            }

            for pr in pull_requests:
                pull_number = pr['number']
                comments = get_review_comments(owner, repo_name, pull_number)
                if not comments:
                    continue  # No review comments found, move to the next pull request
                
                pr_data = {
                    "pull_request_number": pull_number,
                    "comments": comments
                }

                repo_data["pull_requests"].append(pr_data)

            batch_data.append(repo_data)

            if len(batch_data) >= batch_size:
                processed_repos.extend(batch_data)
                batch_data = []

        else:
            continue  # Skip repository if pull request count is not within the desired range

    # Write any remaining data in the batch to JSON file
    if batch_data:
        processed_repos.extend(batch_data)

    # Write the accumulated data to the JSON file
    with open('output.json', 'w') as json_file:
        json.dump(processed_repos, json_file, indent=4)
        print("Data written to output.json")

if __name__ == "__main__":
    main()
