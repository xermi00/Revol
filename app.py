import requests
import json
from flask import Flask, request

app = Flask(__name__)

# GitHub configuration
GITHUB_TOKEN = "your_personal_access_token"  # Replace with your PAT
GITHUB_REPO = "username/repository-name"    # Replace with your repo name
GITHUB_BRANCH = "main"                      # Replace with your branch name
FILE_PATH = "user_data.txt"                 # Path in the repo where the file will be stored

@app.route('/update', methods=['POST'])
def update_data():
    # Get form data
    username = request.form.get('username')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    if not all([username, latitude, longitude]):
        return "Invalid input", 400

    # Append data to the file locally
    log_entry = f"Username: {username}, Latitude: {latitude}, Longitude: {longitude}\n"
    with open("user_data.txt", "a") as file:
        file.write(log_entry)

    # Read current file content from GitHub (if it exists)
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:  # File exists
        content_data = response.json()
        sha = content_data["sha"]  # Required for updates
        current_content = requests.get(content_data["download_url"]).text
        updated_content = current_content + log_entry
    else:  # File does not exist
        sha = None
        updated_content = log_entry

    # Update file on GitHub
    payload = {
        "message": "Update user data",
        "content": updated_content.encode("utf-8").decode("latin1"),
        "branch": GITHUB_BRANCH,
    }
    if sha:
        payload["sha"] = sha

    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code in [200, 201]:
        return "Data successfully logged and pushed to GitHub"
    else:
        return f"Failed to update GitHub: {response.json()}", 500


if __name__ == "__main__":
    app.run(debug=True)
