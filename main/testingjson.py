import json

# Sample data
sample_data = [
    {
        "repository": "user1/repo1",
        "pull_requests": [
            {"pull_number": 1, "comment": "This is a comment for PR #1"},
            {"pull_number": 2, "comment": "Another comment for PR #2"}
        ]
    },
    {
        "repository": "user2/repo2",
        "pull_requests": [
            {"pull_number": 3, "comment": "Comment for PR #3"}
        ]
    }
]

try:
    # Open the file for writing
    with open(r'C:\Users\Nikita\PIL\sample_output.json', 'w') as json_file:
        # Write sample data to JSON file
        json.dump(sample_data, json_file, indent=4)
    print("Sample data written to output.json.")
except Exception as e:
    # If an error occurs, print it
    print("Error:", e)
