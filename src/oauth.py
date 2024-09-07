





import msal
import requests
from flask import Flask, redirect, request

app = Flask(__name__)

# Configuration parameters
# Initialize OAuth session
client_id = 'b1d6852b-fb3f-435a-ab82-a7e5bcbe04b0'
client_secret = '43aac305-5d7c-466e-a4b6-03047c827015'
tenant_id = '3f65100d-6d42-4737-8d83-3c9b1c7b56f8'

authority = f'https://login.microsoftonline.com/{tenant_id}'
redirect_uri = 'http://localhost:8000/get_token'
scope = [f'https://{tenant_id}.sharepoint.com/.default']

# Initialize MSAL
msal_app = msal.PublicClientApplication(
    client_id,
    authority=authority,
    token_cache=msal.SerializableTokenCache()
)

@app.route('/login')
def login():
    auth_url = msal_app.get_authorization_request_url(
        scopes=scope,
        redirect_uri=redirect_uri
    )
    return redirect(auth_url)

@app.route('/get_token')
def get_token():
    code = request.args.get('code')
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=scope,
        redirect_uri=redirect_uri
    )
    if "access_token" in result:
        access_token = result['access_token']
        sharepoint_data = get_sharepoint_data(access_token)
        return f"SharePoint Data: {sharepoint_data}"
    else:
        return f"Error: {result.get('error_description')}"

def get_sharepoint_data(access_token):
    url = f'https://{tenant_id}.sharepoint.com/_api/web/lists'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json;odata=verbose'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} {response.text}"

if __name__ == "__main__":
    app.run(port=8000)