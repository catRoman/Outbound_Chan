from msal import PublicClientApplication

import pandas as pd
from io import BytesIO
import requests


app = PublicClientApplication(
    "b1d6852b-fb3f-435a-ab82-a7e5bcbe04b0",
    authority="https://login.microsoftonline.com/3f65100d-6d42-4737-8d83-3c9b1c7b56f8"
)

# initialize result variable to hole the token response
oauth_token = None

# We now check the cache to see
# whether we already have some accounts that the end user already used to sign in before.
accounts = app.get_accounts()
if accounts:
    # If so, you could then somehow display these accounts and let end user choose
    print("Pick the account you want to use to proceed:")
    for a in accounts:
        print(a["username"])
    # Assuming the end user chose this one
    chosen = accounts[0]
    # Now let's try to find a token in cache for this account
    oauth_token = app.acquire_token_silent(["User.Read"], account=chosen)

if not oauth_token:
    # So no suitable token exists in cache. Let's get a new one from Azure AD.
    oauth_token = app.acquire_token_interactive(scopes=["User.Read"]
                                                )
if "access_token" in oauth_token:
    print(oauth_token["access_token"])  # Yay!
else:
    print(oauth_token.get("error"))
    print(oauth_token.get("error_description"))
    print(oauth_token.get("correlation_id"))  # You may need this when reporting a bug




# Define constants
  # Replace with your actual OAuth token
search_query = 'Sep-Obws.xlsm'  # File name to search for

# Define the API endpoint
graph_api_url = f'https://graph.microsoft.com/v1.0/me/drive/root/search(q=\'{search_query}\')'

# Set up the request headers
headers = {
    'Authorization': f'Bearer {oauth_token}'
}

# Make the request to search for the file
response = requests.get(graph_api_url, headers=headers)

if response.status_code == 200:
    results = response.json().get('value', [])
    if results:
        for item in results:
            print(f"Found file: {item['name']} at {item['parentReference']['path']}")
            # You can store the item ID or path for further operations
            file_id = item['id']
            file_path = item['parentReference']['path'] + '/' + item['name']
            print(f"File ID: {file_id}, File Path: {file_path}")
    else:
        print("No files found.")
else:
    print(f"Failed to search files: {response.status_code}")
    print(response.json())
